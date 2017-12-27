class Monoid:
    """An element in the monoid Q
    """ 
        
    def __init__(self, a = 0, b = 0, c = 0, d = 0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.reduce()
            
    def __mul__(self, other):
        value = map(lambda x: x[0] + x[1], zip(self.value, other.value))
        return Monoid(*value)

    def __repr__(self):
        ans = []
        for var, order in zip("abcd", self.value):
            if order > 0: ans.append("{}^{}".format(var, order))
        if ans: return ' x '.join(ans)
        else: return "1"
    
    @property
    def value(self):
        return (self.a, self.b, self.c, self.d)

    def _unchange(self, old_value):
        return old_value == self.value

    def is_win(self):
        win = [(1, 0, 0, 0),
               (0, 2, 0, 0),
               (0, 1, 1, 0),
               (0, 0, 2, 0)]
        if self.value in win: return True
        else: return False

    def reduce(self):
        rules = self._get_reduce_rules()
        while True:
            old_value = self.value
            for rule in rules:
                rule()
            if self._unchange(old_value): break

    def _get_reduce_rules(self):
        rules = []
        counter = 1
        while True:
            try:
                rules.append(getattr(self, "_reduce_rule_{}".format(counter)))
                counter += 1
            except AttributeError:
                break
        return rules

    def _reduce_rule_1(self):
        self.a %= 2

    def _reduce_rule_2(self):
        if self.b == 0:
            pass
        elif self.b % 2 == 0:
            self.b = 2
        elif self.b % 2 == 1:
            self.b = 1

    def _reduce_rule_3(self):
        if self.c > 0:
            self.b %= 2

    def _reduce_rule_4(self):
        if self.c > 2:
            self.a += self.c - 2
            self.c = 2

    def _reduce_rule_5(self):
        if self.d > 0:
            self.b %= 2

    def _reduce_rule_6(self):
        if self.d > 0:
            self.a += self.c
            self.c = 0

    def _reduce_rule_7(self):
        self.c += (self.d // 2) * 2
        self.d %= 2
