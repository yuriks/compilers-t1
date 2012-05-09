import ast

class ParseError(Exception):
    pass

class TokenPeek:
    def __init__(self, token_gen):
        self.token_iter = iter(token_gen)
        self.top = next(self.token_iter)

    def peek(self):
        return self.top

    def next(self):
        try:
            self.top = next(self.token_iter)
        except StopIteration:
            self.top = ('@@eof', None)

    def pop(self):
        tmp = self.peek()
        self.next()
        return tmp

    def expect(self, tok_id):
        t, v = self.pop()
        if t != tok_id:
            raise ParseError("Expected %s; got %s." % (tok_id, t))
        return v

def parse_token_decl(tokens):
    token_id = tokens.expect('@token-id')
    tokens.expect('@$:=')
    token_match = tokens.expect('@token-match')

    return ast.TokenDefinition(token_id, token_match)

def parse_rule_decl(tokens):
    rule_id = tokens.expect('@rule-id')
    tokens.expect('@$:=')
    rule_expr = parse_alternation_expr(tokens)

    return ast.RuleDefinition(rule_id, rule_expr)

def parse_atom(tokens):
    t, v = tokens.pop()
    if t in ('@token-id', '@rule-id'):
        return ast.RuleTokenId(v)
    elif t == '@token-literal':
        return ast.TokenLiteral(v)
    elif t == '@$(':
        expr = parse_alternation_expr(tokens)
        tokens.expect('@$)')
        return expr
    else:
        raise ParseError("Expected @token-id, @rule-id, @token-literal or @$(; got %s." % (t,))

def parse_postfix_expr(tokens):
    expr = parse_atom(tokens)
    t, v = tokens.peek()
    if t == '@$?':
        post_type = '?'
        tokens.next()
    elif t == '@$*':
        post_type = '*'
        tokens.next()
    else:
        post_type = None

    return ast.PostfixExpr(post_type, expr)

def parse_follow_expr(tokens):
    exprs = [parse_postfix_expr(tokens)]
    while True:
        t, v = tokens.peek()
        if t != '@$=>':
            break
        tokens.next()
        exprs.append(parse_postfix_expr(tokens))

    return ast.FollowExpr(exprs)

def parse_alternation_expr(tokens):
    exprs = [parse_follow_expr(tokens)]
    while True:
        t, v = tokens.peek()
        if t != '@$|':
            break
        tokens.next()
        exprs.append(parse_follow_expr(tokens))

    return ast.AlternationExpr(exprs)

def parse_grammar_rule(tokens):
    stmts = []

    t, v = tokens.peek()
    while t != '@@eof':
        if t == '@token-id':
            stmts.append(parse_token_decl(tokens))
        elif t == '@rule-id':
            stmts.append(parse_rule_decl(tokens))
        else:
            raise ParseError("Expected @token-id or @rule-id; got %s." % (t,))

        tokens.expect('@$;')
        t, v = tokens.peek()

    return ast.Root(stmts)

def parse_grammar(token_iter):
    return parse_grammar_rule(TokenPeek(token_iter))

__all__ = ['parse_grammar', 'ParseError']
