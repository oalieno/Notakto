from .constants import BOARD_TEMPLATE

class Result:
    def __init__(self, status, index, x, y):
        self.status = status
        self.index = index
        self.x = x
        self.y = y

    @property
    def move(self):
        return (self.index, self.x, self.y)

    def __repr__(self):
        return "Result({}, {}, {}, {})".format(self.status, self.index, self.x, self.y)

    def __str__(self):
        ans = ("Current Monoid: {}\n"
               "Winning Position? {}\n"
               "Last move was at the {} board\n").format(self.status, self.status.is_win(), self.index)
        stones = [' '] * 9
        stones[self.x * 3 + self.y] = 'X'
        ans += BOARD_TEMPLATE.format(*stones)
        return ans
