from my_ast import AssignmentNode, IfNode, WhileNode, BuiltinNode
from cfg import CFG, ast_to_cfg
from visualize import visualize_cfg

# 构造复杂的 AST 示例
ast = [
    # 初始化变量
    AssignmentNode("x", "10"),
    AssignmentNode("y", "0"),
    AssignmentNode("z", "1"),

    # 外层循环
    WhileNode("x > 0", [
        # 嵌套条件分支
        IfNode("x % 2 == 0",
               then_branch=[
                   AssignmentNode("y", "y + z"),
                   BuiltinNode("write", ["Even branch executed"])
               ],
               else_branch=[
                   AssignmentNode("z", "z * 2"),
                   BuiltinNode("write", ["Odd branch executed"])
               ]),

        # 减少 x
        AssignmentNode("x", "x - 1"),

        # 内层循环
        WhileNode("z > 10", [
            AssignmentNode("z", "z - 5"),
            BuiltinNode("write", ["Inner loop executed"])
        ])
    ]),

    # 循环结束后调用内置函数
    BuiltinNode("write", ["Computation Complete"]),
]

# 转换 AST 为 CFG
cfg = CFG()
current_block = None
for stmt in ast:
    current_block = ast_to_cfg(stmt, cfg, current_block)

# 打印 CFG 和可视化
print(cfg)
visualize_cfg(cfg)
