class Grammar:
    def __init__(self):
        self.rules = {}
        self.token = set()

        self.rule_unique_nums = {}
        self.token_literals = set()

    def generate_temp_name(self, rule_name):
        num = self.rule_unique_nums.get(rule_name, 0) + 1
        self.rule_unique_nums[rule_name] = num
        return '%s$%d' % (rule_name, num)
