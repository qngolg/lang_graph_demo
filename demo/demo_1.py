import os
from typing import Annotated, TypedDict, List, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import asyncio

from dotenv import load_dotenv

load_dotenv()
# --------------------------
# 1. 定义状态类型
# --------------------------
class GraphState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    current_step: str
    partial_response: str  # 用于累积流式生成的片段
    is_complete: bool

# --------------------------
# 2. 初始化大模型（支持流式）
# --------------------------

api_key = os.getenv("aliyun_sk")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = "gpt-3.5-turbo"

llm = ChatOpenAI(
    model="qwen-plus",
    api_key=api_key,
    base_url=base_url,
    temperature=0.7)

# --------------------------
# 3. 定义节点：调用大模型并流式生成
# --------------------------
async def generate_answer_streaming(state: GraphState) -> GraphState:
    print("\n🤖 [节点] 开始流式生成答案...")
    state["current_step"] = "generating"
    state["partial_response"] = ""

    # 构造输入消息
    user_msg = next((m.content for m in state["messages"] if isinstance(m, HumanMessage)), "")
    ai_message = HumanMessage(content=user_msg)  # 简化，实际应该构造合适的 Message 列表
    messages = [HumanMessage(content=user_msg)]  # 你可以按需构造 prompt

    # 调用流式大模型
    full_response = ""
    stream = llm.stream(messages)  # 返回的是 AIMessageChunk 的生成器

    print("📤 开始流式输出（逐步打印）:")
    async for chunk in stream:
        content = chunk.content
        if content:
            print(content, end="", flush=True)  # 实时打印每个 token
            full_response += content
            state["partial_response"] += content  # 累积到状态中，可被后续节点使用

    print("\n✅ [节点] 流式生成完成")
    state["messages"].append(AIMessage(content=full_response))  # 把完整回复加入消息历史
    state["is_complete"] = True  # 表示此步骤完成，图可以进入下一步
    return state

# --------------------------
# 4. 定义其他节点（如开始、结束等）
# --------------------------
def start(state: GraphState) -> GraphState:
    print("🚀 开始执行图")
    return {
        "messages": [HumanMessage(content="请介绍一下大语言模型的原理。")],
        "current_step": "start",
        "partial_response": "",
        "is_complete": False
    }

def end(state: GraphState) -> GraphState:
    print("\n🎯 图执行完毕，最终回复:")
    final_msg = state["messages"][-1].content if state["messages"] else "无回复"
    print(final_msg)
    return {
        "messages": state["messages"],
        "current_step": "end",
        "partial_response": state["partial_response"],
        "is_complete": True
    }

# --------------------------
# 5. 构建图
# --------------------------
workflow = StateGraph(GraphState)

workflow.add_node("start", start)
workflow.add_node("generate", generate_answer_streaming)  # 流式节点
workflow.add_node("end", end)

workflow.set_entry_point("start")
workflow.add_edge("start", "generate")
workflow.add_edge("generate", "end")

app = workflow.compile()

# --------------------------
# 6. 运行图
# --------------------------
asyncio.run(app.invoke({}))