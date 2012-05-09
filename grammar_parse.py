import ast

class ParseError(Exception):
    pass

def parse_grammar(token_iter):
    return ast.Root([])

__all__ = ['parse_grammar', 'ParseError']
