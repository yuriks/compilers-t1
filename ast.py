"""
Classes representing the parsed grammar AST.
"""

class Node:
    pass

class Root(Node):
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return ' ;\n'.join(map(str, self.statements)) + ' ;\n'

class TokenDefinition(Node):
    def __init__(self, name, regexp):
        self.name = name
        self.regexp = regexp

    def __str__(self):
        return self.name + ' := "' + str(self.regexp) + '"'

class RuleDefinition(Node):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return self.name + ' := ' + str(self.expression)

class AlternationExpr(Node):
    def __init__(self, expressions):
        self.expressions = expressions

    def __str__(self):
        return '( ' + ' | '.join(map(str, self.expressions)) + ' )'

class FollowExpr(Node):
    def __init__(self, expressions):
        self.expressions = expressions

    def __str__(self):
        return '( ' + ' => '.join(map(str, self.expressions)) + ' )'

class PostfixExpr(Node):
    def __init__(self, operator, expression):
        self.expression = expression
        # Either '?', '*' or None
        self.operator = operator

    def __str__(self):
        if self.operator is not None:
            return str(self.expression) + self.operator
        else:
            return str(self.expression)

class TokenLiteral(Node):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "'%s'" % (self.text,)

class RuleTokenId(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
