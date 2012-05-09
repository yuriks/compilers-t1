import ast
import ast_simplify
import lexer

class Grammar:
    def __init__(self):
        self.rules = {}
        self.tokens = {}

        self.rule_unique_nums = {}
        self.token_literals = set()

        self.lexer = None

    def generate_temp_name(self, rule_name):
        num = self.rule_unique_nums.get(rule_name, 0) + 1
        self.rule_unique_nums[rule_name] = num
        return '$%s$%d' % (rule_name, num)

    def load_from_ast(self, ast_root):
        for st in ast_root.statements:
            if isinstance(st, ast.TokenDefinition):
                self.tokens[st.name] = st.regexp
            elif isinstance(st, ast.RuleDefinition):
                self.rules[st.name] = ast_simplify.convert_ast_to_rule(self, st.name, st.expression)

        lexer.add_literal_tokens(self.tokens, self.token_literals)
        self.lexer = lexer.Tokenizer(self.tokens)
