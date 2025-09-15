# LangGraph Demo
## 初始化
1. 创建conda虚拟环境
```shell
conda create --name langgraph_311 python==3.11
```

2. 安装UV包管理器（下载包快）
```shell
pip install uv
```
3. 使用uv初始化工程
```shell
cd .. # 返回上级目录
uv init lang_graph_demo # 此时会生成一个pyproject.toml
```
4. 在pyproject.toml中添加相应的依赖
```toml
[project]
name = "lang-graph-demo"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "flask",
    "langchain",
    "langchain-openai",
    "langchain-core",
    "langgraph"
]

```

5. 安装所需的包
```shell
cd lang_graph_demo
uv pip install . 
```