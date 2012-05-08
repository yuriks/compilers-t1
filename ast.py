"""
Functions for creating nodes representing the parsed grammar AST.

These exist mostly for purposes of documentation, and because they're more
terse than classes.
"""

class Node:
    def __init__(self, kind):
        self.kind = kind

def Root(statements):
    self = Node("Root")
    self.statements = statements
    return self

def TokenDefinition(name, regexp):
    self = Node("TokenDefinition")
    self.name = name
    self.regexp = regexp
    return self

def RuleDefinition(name, expression):
    self = Node("RuleDefinition")
    self.name = name
    self.expression = expression
    return self

def AlternationExpr(expressions):
    self = Node("AlternationExpr")
    self.expressions = expressions
    return self

def FollowExpr(expressions):
    self = Node("FollowExpr")
    self.expressions = expressions
    return self

def PostfixExpr(operator, expression):
    self = Node("PostfixExpr")
    self.expression = expression
    # Either '?', '*' or None
    self.operator = operator
    return self

def Atom(expression):
    self = Node("Atom")
    self.expression = expression
    return self

def TokenLiteral(text):
    self = Node("TokenLiteral")
    self.text = text
    return self

def RuleTokenId(name):
    self = Node("RuleTokenId")
    self.name = name
    return self
