import os
from graphviz import Digraph

def visualize_cfg(cfg):
    # 明确指定 Graphviz 可执行文件的路径
    os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'
    
    dot = Digraph()
    for node, edges in cfg.graph.items():
        dot.node(str(node), str(node))
        for edge in edges:
            dot.edge(str(node), str(edge))
    
    # 渲染控制流图
    dot.render('cfg', view=True)
