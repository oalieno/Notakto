import random
from functools import reduce

import exceptions
from constants import PATTERN
from utils import board_to_int, has_line
from Monoid import Monoid

BOARD_WIDTH = 3

class Notakto:
    """notakto solver engine
    """

    def __init__(self, boards):
        """constructor

        Parameters
        ----------
        boards : list of list of list of int
        """
        self.boards = boards

    @property
    def status(self):
        return reduce(lambda x, y: x * y, map(lambda x: PATTERN[board_to_int(x)], self.boards))
   
    @staticmethod
    def _has_line(board):
        for i in range(BOARD_WIDTH):
            if all([board[i][k] for k in range(BOARD_WIDTH)]): return True
            if all([board[k][i] for k in range(BOARD_WIDTH)]): return True
        if all([board[k][k] for k in range(BOARD_WIDTH)]): return True
        if all([board[k][BOARD_WIDTH - 1 - k] for k in range(BOARD_WIDTH)]): return True
        return False

    @staticmethod
    def _index_to_int(index, x, y):
        return index * 9 + x * 3 + y

    @staticmethod
    def _int_to_index(value):
        return (value // 9, *map(lambda x: x % 3, [value // 3, value]))

    def _next_index(self, index, x, y):
        value = self._index_to_int(index, x, y)
        value = (value + 1) % (len(self.boards) * 9)
        return self._int_to_index(value)
        
    def _is_invalid(self, index, x, y):
        if not (0 <= index < len(self.boards)):
            return True
        if not (0 <= x < BOARD_WIDTH):
            return True
        if not (0 <= y < BOARD_WIDTH):
            return True
        return False

    def _is_occupied(self, index, x, y):
        return self.boards[index][x][y] == 1
    
    def _is_dead_board(self, index):
        return self._has_line(self.boards[index])

    def move_check(self, index, x, y):
        if self._is_invalid(index, x, y):
            raise exceptions.InvalidMoveError
        if self._is_occupied(index, x, y):
            raise exceptions.GridOccupiedError
        if self._is_dead_board(index):
            raise exceptions.DeadBoardError

    def move(self, index, x, y, virtual = False):
        self.move_check(index, x, y)
        self.boards[index][x][y] = 1
        status = self.status.is_win()
        if virtual: self.boards[index][x][y] = 0
        return status

    def move_random(self):
        index = random.randrange(0, len(self.boards))
        x = random.randrange(0, BOARD_WIDTH)
        y = random.randrange(0, BOARD_WIDTH)
        for _ in range(len(self.boards) * 9):
            try:
                self.move(index, x, y)
                return (index, x, y)
            except exceptions.DeadBoardError:
                index, x, y = (index + 1) % len(self.boards), 0, 0
            except exceptions.NotaktoError:
                index, x, y = self._next_index(index, x, y)
        raise exceptions.NoAvailableMoveError

    def move_optimize(self):
        for k in range(len(self.boards)):
            for i in range(BOARD_WIDTH):
                for j in range(BOARD_WIDTH):
                    try:
                        if self.move(k, i, j, virtual = True):
                            self.move(k, i, j)
                            return (k, i, j)
                    except exceptions.NotaktoError:
                        pass
        self.move_random()
