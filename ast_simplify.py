"""
Functions to simplify an AST down to a more concise representation.
"""

def simplify(node):
    func = simplification_functions.get(node.kind)
    if func is None:
        return node
    else:
        return func(node)


def simplify_AlternationExpr(node):
    sub_exprs = AlternationExpr([simplify(x) for x in node.expressions])

    if len(sub_exprs) == 1:
        return sub_exprs[0]
    else:
        return sub_exprs

def simplify_FollowExpr(node):
    sub_exprs = FollowExpr([simplify(x) for x in node.expressions])

    if len(sub_exprs) == 1:
        return sub_exprs[0]
    else:
        return sub_exprs

def simplify_PostfixExpr(node):
    sub_expr = simplify(node.expression)

    if node.operator is None:
        return sub_expr
    else:
        return PostfixExpr(sub_expr, node.operator)

def simplify_Atom(node):
    return simplify(node.expression)

simplification_functions = {
        "AlternationExpr": simplify_AlternationExpr,
        "FollowExpr": simplify_FollowExpr,
        "PostfixExpr": simplify_PostfixExpr,
        "Atom": simplify_Atom
    }
