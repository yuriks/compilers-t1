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

def tested_update(dest_set, src_set):
    result_set = dest_set.union(src_set)
    has_changed = dest_set != result_set
    dest_set.update(src_set)
    return has_changed

def follow(rules):
    follow_sets = {}

    for rule in rules:
        if rule[0] == '#': # starting rule
            follow_sets[rule] = {'@@eof'}
        else:
            follow_sets[rule] = set()

    changed = True
    while changed:
        changed = False
        for rule in rules:
            for production in rules[rule]:
                for i in range(len(production)-1):
                    if production[i][0] != '@':
                        first_set = first(production[i+1], rules)
                        changed = changed or tested_update(
                            follow_sets[production[i]], first_set-{'@@e'})
                        if '@@e' in first_set:
                            changed = changed or tested_update(
                                follow_sets[production[i]], follow_sets[rule])

                if production[-1][0] != '@':
                    changed = changed or tested_update(
                        follow_sets[production[-1]], follow_sets[rule])

    return follow_sets
