class ASTNode:
    pass

class AssignmentNode(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return f"{self.variable} = {self.expression}"

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"if {self.condition} then ... else ..."

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while {self.condition} do ..."

class BuiltinNode(ASTNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

    def __repr__(self):
        return f"{self.function}({', '.join(self.arguments)})"
