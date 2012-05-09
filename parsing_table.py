def build_parse_table(grammar):
    table = {}
    for rule in grammar.rules:
        for prod in grammar[rule]:
            for ft in first(prod, grammar):
                self.table[(grammar[rule], ft)] = prod
            for fl in follow(prod, grammar):
                self.table[(grammar[rule], fl)] = prod

def first(symbol, rules):
    if symbol[0] == '@': # terminal (also handles empty '@@e')
        return {symbol}
    else: # non-terminal
        first_set = set()

        for production in rules[symbol]:
            add_e = True
            for prod_symbol in production:
                prod_first = first(prod_symbol, rules)
                first_set.update(prod_first - {'@@e'})
                if '@@e' not in prod_first:
                    add_e = False
                    break
            if add_e:
                first_set.add('@@e')

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
