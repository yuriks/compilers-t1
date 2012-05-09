"""
Functions to simplify a grammar AST.
"""

import ast

"""Converts AST node representing an expression to list of productions format."""
def convert_ast_to_rule(grammar, rule_name, node):
    simplified_node = simplify(grammar, rule_name, node)

    if isinstance(simplified_node, ast.AlternationExpr):
        alternation_expr = simplified_node
    elif isinstance(simplified_node, ast.FollowExpr):
        alternation_expr = ast.AlternationExpr([simplified_node])
    else:
        alternation_expr = ast.AlternationExpr([ast.FollowExpr([simplified_node])])

    return [[y.name for y in x.expressions] for x in alternation_expr.expressions]

def simplify(grammar, rule_name, node):
    func = simplification_functions.get(type(node))
    if func is None:
        return node
    else:
        return func(grammar, rule_name, node)

def simplify_AlternationExpr(grammar, rule_name, node):
    sub_exprs = [simplify(grammar, rule_name, x) for x in node.expressions]

    associated_exprs = []
    for expr in sub_exprs:
        if isinstance(expr, ast.AlternationExpr):
            associated_exprs += expr.expressions
        else:
            associated_exprs.append(expr)

    def ensure_FollowExpr(expr):
        if isinstance(expr, ast.FollowExpr):
            return expr
        else:
            return ast.FollowExpr([expr])

    follow_exprs = list(map(ensure_FollowExpr, associated_exprs))

    if len(follow_exprs) == 1:
        return follow_exprs[0]
    else:
        return ast.AlternationExpr(follow_exprs)

def simplify_FollowExpr(grammar, rule_name, node):
    sub_exprs = [simplify(grammar, rule_name, x) for x in node.expressions]

    associated_exprs = []
    for expr in sub_exprs:
        if isinstance(expr, ast.FollowExpr):
            associated_exprs += expr.expressions
        else:
            associated_exprs.append(expr)

    def ensure_named_expr(expr):
        if isinstance(expr, ast.RuleTokenId):
            return expr
        else:
            tmp_name = grammar.generate_temp_name(rule_name)
            grammar.rules[tmp_name] = convert_ast_to_rule(grammar, tmp_name, expr)
            return ast.RuleTokenId(tmp_name)

    named_exprs = list(map(ensure_named_expr, associated_exprs))

    if len(named_exprs) == 1:
        return named_exprs[0]
    else:
        return ast.FollowExpr(named_exprs)

def simplify_PostfixExpr(grammar, rule_name, node):
    if node.operator == '?':
        new_expr = ast.AlternationExpr([node.expression, ast.RuleTokenId('@@e')])
    elif node.operator == '*':
        tmp_name = grammar.generate_temp_name(rule_name)

        tmp_node = ast.AlternationExpr([
            ast.FollowExpr([node.expression, ast.RuleTokenId(tmp_name)]),
            ast.RuleTokenId('@@e')])

        new_expr = ast.RuleTokenId(tmp_name)
        grammar.rules[tmp_name] = convert_ast_to_rule(grammar, tmp_name, tmp_node)
    elif node.operator is None:
        new_expr = node.expression

    return simplify(grammar, rule_name, new_expr)

def simplify_TokenLiteral(grammar, rule_name, node):
    grammar.token_literals.add(node.text)
    return ast.RuleTokenId('@$' + node.text)

simplification_functions = {
        ast.AlternationExpr: simplify_AlternationExpr,
        ast.FollowExpr: simplify_FollowExpr,
        ast.PostfixExpr: simplify_PostfixExpr,
        ast.TokenLiteral: simplify_TokenLiteral
    }
