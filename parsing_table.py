class ParsingTable:
    def __init__(self, grammar):
        pass
#       tokens = grammar.tokens #TODO: get them real values
#       table = {} # key: (token, rule name), value: what to do
#       for rname, productions in grammar.rules.items():
#            for token in symbols:
#                pass

def first(x, rules):
    emtpy = '@@e'

    if x[0] == '@': #terminals begin with @
        return {x}
    elif x[0] == empty:
        return { empty }
    else:
        first_set = set()
        prods = rules[x]
        
        for prod in rules[x]:
            tmp_prodfirst = first(prod, rules) 
            first_set = first_set.union({f for f in tmp_prodfirst if f != empty})
            if empty not in tmp_prodfirst:
                break
        return first_se                                   
