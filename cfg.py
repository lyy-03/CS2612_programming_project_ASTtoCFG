from my_ast import AssignmentNode, IfNode, WhileNode, BuiltinNode

class CFGNode:
    def __init__(self, ast_node):
        self.ast_node = ast_node

    def __repr__(self):
        return repr(self.ast_node)

class CFG:
    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.graph = {}
        self.basic_blocks = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            self.edges[node] = []

    def add_edge(self, from_node, to_node):
        if from_node not in self.nodes:
            self.add_node(from_node)
        if to_node not in self.nodes:
            self.add_node(to_node)
        self.edges[from_node].append(to_node)
        if from_node not in self.graph:
            self.graph[from_node] = []
        self.graph[from_node].append(to_node)

    def add_to_block(self, block_name, content):
        """向指定基本块中添加指令"""
        if block_name not in self.basic_blocks:
            self.basic_blocks[block_name] = []
        self.basic_blocks[block_name].append(content)

    def __repr__(self):
        result = []
        for node, edges in self.edges.items():
            result.append(f"{node} -> {edges}")
        return "\n".join(result)
    
    def __str__(self):
        result = []
        for node, edges in self.graph.items():
            result.append(f"{node} -> {edges}")
            if node in self.basic_blocks:
                result.append(f"  Content: {self.basic_blocks[node]}")
        return "\n".join(result)

def ast_to_cfg(ast_node, cfg, current_block=None):
    if isinstance(ast_node, AssignmentNode):
        if current_block is None:
            current_block = CFGNode("block_0")
            cfg.add_node(current_block)
        cfg.add_to_block(current_block, f"{ast_node.variable} = {ast_node.expression}")
        return current_block

    elif isinstance(ast_node, IfNode):
        condition_node = CFGNode(ast_node)
        cfg.add_node(condition_node)
        if current_block:
            cfg.add_edge(current_block, condition_node)

        # Then branch
        then_entry = CFGNode("then")
        cfg.add_node(then_entry)
        cfg.add_edge(condition_node, then_entry)
        last_then_node = None
        for stmt in ast_node.then_branch:
            last_then_node = ast_to_cfg(stmt, cfg, then_entry if last_then_node is None else last_then_node)

        # Else branch
        else_entry = CFGNode("else")
        cfg.add_node(else_entry)
        cfg.add_edge(condition_node, else_entry)
        last_else_node = None
        for stmt in ast_node.else_branch:
            last_else_node = ast_to_cfg(stmt, cfg, else_entry if last_else_node is None else last_else_node)

        # Merge point
        merge_node = CFGNode("merge")
        cfg.add_node(merge_node)
        if last_then_node:
            cfg.add_edge(last_then_node, merge_node)
        if last_else_node:
            cfg.add_edge(last_else_node, merge_node)

        return merge_node

    elif isinstance(ast_node, WhileNode):
        condition_node = CFGNode(ast_node)
        cfg.add_node(condition_node)
        if current_block:
            cfg.add_edge(current_block, condition_node)

        # Loop body
        loop_entry = CFGNode("loop")
        cfg.add_node(loop_entry)
        cfg.add_edge(condition_node, loop_entry)
        last_loop_node = None
        for stmt in ast_node.body:
            last_loop_node = ast_to_cfg(stmt, cfg, loop_entry if last_loop_node is None else last_loop_node)

        # Back to condition
        if last_loop_node:
            cfg.add_edge(last_loop_node, condition_node)

        # Exit loop
        after_loop_node = CFGNode("after_loop")
        cfg.add_node(after_loop_node)
        cfg.add_edge(condition_node, after_loop_node)

        return after_loop_node

    elif isinstance(ast_node, BuiltinNode):
        current_node = CFGNode(ast_node)
        cfg.add_node(current_node)
        if current_block:
            cfg.add_edge(current_block, current_node)
        return current_node
