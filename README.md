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
4. 添加相应的依赖


5. 安装所需的包
```shell
cd lang_graph_demo
uv pip install . 
```