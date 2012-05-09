class ParsingTable:
    def __init__(self, grammar):
        pass
#       tokens = grammar.tokens #TODO: get them real values
#       table = {} # key: (token, rule name), value: what to do
#       for rname, productions in grammar.rules.items():
#            for token in symbols:
#                pass

def first(x, rules):
    empty = '@@e'

    if x[0] == '@': #terminals begin with @
        return {x}
    elif x == empty:
        return { empty }
    else:
        first_set = set()
        prods = rules[x]
        
        for prod in rules[x]:
            tmp_prodfirst = first(prod, rules) 
            first_set = first_set.union({f for f in tmp_prodfirst if f != empty})
            if empty not in tmp_prodfirst:
                break
        return first_set            

def follow(a, rules):
    follow_set = set()
    empty == '@@e'

    if a[0] == '#':
        follow_set.add('@@eof')
    r_rules = rules.copy()
    del r_rules[a]

    for rname, productions in r_rules:
        for prod in productions:
            try:
                i = prod.index(a) 
                first_beta = first(prop[i + 1])
                follow_set = follow_set.union({b for b in first_beta if b != empty})
                if empty in first_beta:
                    follow_set = follow_set.union(follow(rname))
                follow_set = follow_set.union(follow(prod))
            except ValueError:
                continue  
    return follow_set
