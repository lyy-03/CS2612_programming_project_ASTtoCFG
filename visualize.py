import os
from graphviz import Digraph

def visualize_cfg(cfg):
    # 明确指定 Graphviz 可执行文件的路径
    os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'
    
    dot = Digraph()

    # 为 CFG 节点添加节点和边
    for node, edges in cfg.graph.items():
        dot.node(str(node), label=str(node))
        for edge in edges:
            dot.edge(str(node), str(edge))
    
    # 为基本块内容单独添加节点
    for block, content in cfg.basic_blocks.items():
        block_label = f"{block}\\n" + "\\n".join(content)
        dot.node(str(block), label=block_label)

    # 渲染控制流图
    dot.render('cfg', view=True)
