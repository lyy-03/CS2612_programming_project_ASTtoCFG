from my_ast import AssignmentNode, IfNode, WhileNode, BuiltinNode

global_counter = {"id": 0}

class CFGNode:
    def __init__(self, ast_node, label=None):
        self.ast_node = ast_node
        self.label = label or repr(ast_node)

    def __repr__(self):
        return self.label

class CFG:
    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.graph = {}
        self.basic_blocks = {}

    def add_node(self, node):
        self.nodes.append(node)
        self.edges[node] = []

    def add_edge(self, from_node, to_node):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
        if from_node not in self.graph:
            self.graph[from_node] = []
        self.graph[from_node].append(to_node)

    def add_to_block(self, block_name, content):
        """向指定基本块中添加指令"""
        if block_name not in self.basic_blocks:
            self.basic_blocks[block_name] = []
        self.basic_blocks[block_name].append(content)

    def __str__(self):
        result = []
        for node, edges in self.graph.items():
            result.append(f"{node} -> {edges}")
            if node in self.basic_blocks:
                result.append(f"  Content: {self.basic_blocks[node]}")
        return "\n".join(result)

def get_unique_label(prefix=""):
    """生成全局唯一的标签，带可选前缀"""
    global_counter["id"] += 1
    return f"{prefix}_{global_counter['id']}"

def ast_to_cfg(ast_node, cfg, current_block):
    if isinstance(ast_node, AssignmentNode):
        # 处理赋值语句
        cfg.add_to_block(current_block, f"{ast_node.variable} = {ast_node.expression}")
        return current_block

    elif isinstance(ast_node, BuiltinNode):
        # 处理内置函数调用
        cfg.add_to_block(current_block, f"{ast_node.function}({', '.join(ast_node.arguments)})")
        return current_block

    elif isinstance(ast_node, IfNode):
        # 处理条件分支
        condition_label = get_unique_label("if")
        then_label = get_unique_label("then")
        else_label = get_unique_label("else")
        merge_label = get_unique_label("merge")

        cfg.add_edge(current_block, condition_label)
        cfg.add_to_block(condition_label, ast_node.condition)

        # 处理 then 分支
        cfg.add_edge(condition_label, then_label)
        current_then_block = then_label
        for stmt in ast_node.then_branch:
            current_then_block = ast_to_cfg(stmt, cfg, current_then_block)
        cfg.add_edge(current_then_block, merge_label)

        # 处理 else 分支
        cfg.add_edge(condition_label, else_label)
        current_else_block = else_label
        for stmt in ast_node.else_branch:
            current_else_block = ast_to_cfg(stmt, cfg, current_else_block)
        cfg.add_edge(current_else_block, merge_label)

        return merge_label

    elif isinstance(ast_node, WhileNode):
        # 处理循环
        entry_label = get_unique_label("while")
        loop_label = get_unique_label("loop")
        after_label = get_unique_label("after_loop")

        cfg.add_edge(current_block, entry_label)
        cfg.add_to_block(entry_label, ast_node.condition)

        # 处理循环体
        cfg.add_edge(entry_label, loop_label)
        current_loop_block = loop_label
        for stmt in ast_node.body:
            current_loop_block = ast_to_cfg(stmt, cfg, current_loop_block)
        cfg.add_edge(current_loop_block, entry_label)

        # 处理循环后
        cfg.add_edge(entry_label, after_label)
        return after_label

    else:
        raise ValueError(f"Unknown AST node type: {type(ast_node)}")