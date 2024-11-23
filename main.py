from my_ast import AssignmentNode, IfNode, WhileNode, BuiltinNode
from cfg import CFG, ast_to_cfg
from visualize import visualize_cfg

# 构造复杂的 AST 示例
ast = [
    AssignmentNode("x", "10"),
    WhileNode("x > 0", [
        IfNode("x % 2 == 0", [
            AssignmentNode("y", "y + 1"),
            WhileNode("z > 0", [
                AssignmentNode("z", "z - 1"),
                BuiltinNode("print", ["Inner loop"])
            ])
        ], [
            AssignmentNode("w", "w * 2"),
            BuiltinNode("log", ["Odd branch"])
        ]),
        AssignmentNode("x", "x - 1")
    ]),
    BuiltinNode("print", ["Done"]),
    AssignmentNode("y", "y + 1"),
    AssignmentNode("x", "y + 1"),
    WhileNode("x < 0", [
        IfNode("x % 2 == 0", [
            AssignmentNode("y", "y + 1"),
            WhileNode("z > 0", [
                AssignmentNode("z", "z - 1"),
                BuiltinNode("print", ["Inner loop"])
            ])
        ], [
            AssignmentNode("w", "w * 2"),
            BuiltinNode("log", ["Odd branch"])
        ]),
        AssignmentNode("x", "x - 1")
    ])
]



# 转换 AST 为 CFG
cfg = CFG()
current_block = None
for stmt in ast:
    current_block = ast_to_cfg(stmt, cfg, current_block)

# 打印 CFG 和可视化
print(cfg)
visualize_cfg(cfg)
