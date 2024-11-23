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

    def add_node(self, node):
        self.nodes.append(node)
        self.edges[node] = []

    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)
        if from_node not in self.graph:
            self.graph[from_node] = []
        self.graph[from_node].append(to_node)

    def __repr__(self):
        result = []
        for node, edges in self.edges.items():
            result.append(f"{node} -> {edges}")
        return "\n".join(result)
    
    def __str__(self):
        result = []
        for node, edges in self.graph.items():
            result.append(f"{node} -> {edges}")
        return "\n".join(result)

def ast_to_cfg(ast, cfg, prev_node=None):
    if isinstance(ast, AssignmentNode):
        current_node = CFGNode(ast)
        cfg.add_node(current_node)
        if prev_node:
            cfg.add_edge(prev_node, current_node)
        return current_node

    elif isinstance(ast, IfNode):
        condition_node = CFGNode(ast)
        cfg.add_node(condition_node)
        if prev_node:
            cfg.add_edge(prev_node, condition_node)

        # Then branch
        then_entry = CFGNode("then")
        cfg.add_node(then_entry)
        cfg.add_edge(condition_node, then_entry)
        last_then_node = None
        for stmt in ast.then_branch:
            last_then_node = ast_to_cfg(stmt, cfg, then_entry if last_then_node is None else last_then_node)

        # Else branch
        else_entry = CFGNode("else")
        cfg.add_node(else_entry)
        cfg.add_edge(condition_node, else_entry)
        last_else_node = None
        for stmt in ast.else_branch:
            last_else_node = ast_to_cfg(stmt, cfg, else_entry if last_else_node is None else last_else_node)

        # Merge point
        merge_node = CFGNode("merge")
        cfg.add_node(merge_node)
        if last_then_node:
            cfg.add_edge(last_then_node, merge_node)
        if last_else_node:
            cfg.add_edge(last_else_node, merge_node)

        return merge_node

    elif isinstance(ast, WhileNode):
        condition_node = CFGNode(ast)
        cfg.add_node(condition_node)
        if prev_node:
            cfg.add_edge(prev_node, condition_node)

        # Loop body
        loop_entry = CFGNode("loop")
        cfg.add_node(loop_entry)
        cfg.add_edge(condition_node, loop_entry)
        last_loop_node = None
        for stmt in ast.body:
            last_loop_node = ast_to_cfg(stmt, cfg, loop_entry if last_loop_node is None else last_loop_node)

        # Back to condition
        if last_loop_node:
            cfg.add_edge(last_loop_node, condition_node)

        # Exit loop
        after_loop_node = CFGNode("after_loop")
        cfg.add_node(after_loop_node)
        cfg.add_edge(condition_node, after_loop_node)

        return after_loop_node

    elif isinstance(ast, BuiltinNode):
        current_node = CFGNode(ast)
        cfg.add_node(current_node)
        if prev_node:
            cfg.add_edge(prev_node, current_node)
        return current_node
