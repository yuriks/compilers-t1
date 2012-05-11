def build_parse_table(rules, tokens):
    table = {}
    first_sets = first(rules, tokens)
    follow_sets = follow(rules, first_sets)

    for rule in rules:
        for prod in rules[rule]:
            first_set = first_sets[prod[0]]
            for ft in first_set - {'@@e'}:
                table[(rule, ft)] = prod
            if '@@e' in first_set:
                for fl in follow_sets[rule]:
                    table[(rule, fl)] = prod

    return table

def tested_update(dest_set, src_set):
    result_set = dest_set.union(src_set)
    has_changed = dest_set != result_set
    dest_set.update(src_set)
    return has_changed

def tested_add(dest_set, item):
    if item in dest_set:
        return False
    else:
        dest_set.add(item)
        return True

def first(rules, tokens):
    first_sets = {}

    for token in tokens:
        if not token.startswith('@@'):
            first_sets[token] = {token}
    first_sets['@@e'] = {'@@e'}

    for rule in rules:
        first_sets[rule] = set()

    changed = True
    while changed:
        changed = False
        for rule in rules:
            for production in rules[rule]:
                add_e = True
                for prod_symbol in production:
                    prod_first = first_sets[prod_symbol]
                    changed = changed or tested_update(
                            first_sets[rule], prod_first - {'@@e'})
                    if '@@e' not in prod_first:
                        add_e = False
                        break
                if add_e:
                    changed = changed or tested_add(first_sets[rule], '@@e')

    return first_sets

def follow(rules, first_sets):
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
                        first_set = first_sets[production[i+1]]
                        changed = changed or tested_update(
                            follow_sets[production[i]], first_set-{'@@e'})
                        if '@@e' in first_set:
                            changed = changed or tested_update(
                                follow_sets[production[i]], follow_sets[rule])

                if production[-1][0] != '@':
                    changed = changed or tested_update(
                        follow_sets[production[-1]], follow_sets[rule])

    return follow_sets
