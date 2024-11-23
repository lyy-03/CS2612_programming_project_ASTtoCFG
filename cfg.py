from my_ast import AssignmentNode, IfNode, WhileNode, BuiltinNode

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

def ast_to_cfg(ast, cfg, prev_node=None, context=None):
    context = context or {"while_count": 0}  # 用于标识循环节点

    if isinstance(ast, AssignmentNode):
        block_name = prev_node if prev_node else f"block_{len(cfg.basic_blocks)}"
        cfg.add_to_block(block_name, f"{ast.variable} = {ast.expression}")
        return block_name

    elif isinstance(ast, IfNode):
        condition_node = CFGNode(ast, label=f"if {ast.condition}")
        cfg.add_node(condition_node)
        if prev_node:
            cfg.add_edge(prev_node, condition_node)

        # Then branch
        then_entry = CFGNode("then", label="then")
        cfg.add_node(then_entry)
        cfg.add_edge(condition_node, then_entry)
        last_then_node = None
        for stmt in ast.then_branch:
            last_then_node = ast_to_cfg(stmt, cfg, then_entry if last_then_node is None else last_then_node, context)

        # Else branch
        else_entry = CFGNode("else", label="else")
        cfg.add_node(else_entry)
        cfg.add_edge(condition_node, else_entry)
        last_else_node = None
        for stmt in ast.else_branch:
            last_else_node = ast_to_cfg(stmt, cfg, else_entry if last_else_node is None else last_else_node, context)

        # Merge point
        merge_node = CFGNode("merge", label="merge")
        cfg.add_node(merge_node)
        if last_then_node:
            cfg.add_edge(last_then_node, merge_node)
        if last_else_node:
            cfg.add_edge(last_else_node, merge_node)

        return merge_node

    elif isinstance(ast, WhileNode):
        # Unique loop entry/exit nodes
        context["while_count"] += 1
        loop_id = context["while_count"]
        condition_node = CFGNode(ast, label=f"while {ast.condition} (#{loop_id})")
        cfg.add_node(condition_node)
        if prev_node:
            cfg.add_edge(prev_node, condition_node)

        # Loop body
        loop_entry = CFGNode(f"loop_{loop_id}", label=f"loop_{loop_id}")
        cfg.add_node(loop_entry)
        cfg.add_edge(condition_node, loop_entry)
        last_loop_node = None
        for stmt in ast.body:
            last_loop_node = ast_to_cfg(stmt, cfg, loop_entry if last_loop_node is None else last_loop_node, context)

        # Back to condition
        if last_loop_node:
            cfg.add_edge(last_loop_node, condition_node)

        # Exit loop
        after_loop_node = CFGNode(f"after_loop_{loop_id}", label=f"after_loop_{loop_id}")
        cfg.add_node(after_loop_node)
        cfg.add_edge(condition_node, after_loop_node)

        return after_loop_node

    elif isinstance(ast, BuiltinNode):
        current_node = CFGNode(ast)
        cfg.add_node(current_node)
        if prev_node:
            cfg.add_edge(prev_node, current_node)
        return current_node
