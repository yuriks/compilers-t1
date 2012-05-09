class GrammarError(Exception):
    pass

class ParseException(Exception):
    def __init__(self, got):
        self.got = got

    def __str__(self):
        return "Unexpected token %s." % (self.got,)


def parse_grammar(grammar, token_stream):
    # TODO remove
    grammar.table = {
        ('#S', '@('): ['@(', '#S', '@+', 'F', '@)'],
        ('#S', '@a'): ['F'],
        ('F',  '@a'): ['@a']
    }

    initial_rule = list(filter(lambda r: r[0] == '#', grammar.rules))
    if len(initial_rule) != 1:
        raise GrammarError("Grammar must have exactly one initial rule. (Name begins with '#'.)")
    initial_rule = initial_rule[0]

    stack = ["@@eof", initial_rule]
    token_iter = iter(token_stream)
    token = next(token_iter)

    while True:
        print("Stack:", stack , "Input:", token)

        token_type, token_data = token
        stack_top = stack.pop()

        if stack_top == token_type:
            if token_type == "@@eof":
                break
            else:
                token = next(token_iter)
        else:
            rule = grammar.table.get((stack_top, token_type), None)
            if rule is None:
                raise ParseException(token)
            stack += rule[::-1]
