import random
from functools import reduce

from .exceptions import NotaktoError, InvalidMoveError, GridOccupiedError, DeadBoardError, NoAvailableMoveError
from .constants import BOARD_WIDTH
from .pattern import PATTERN
from .utils import board_to_int
from .Monoid import Monoid
from .Result import Result

class Notakto:
    """notakto AI

    Example
    -------

        >>> notakto = Notakto([empty_board()])
        >>> result = notakto.move_optimize()

        >>> result
        Result(c^2, 0, 1, 1)
        >>> print(result)
        Current Monoid: c^2
        Winning Position? True
        Last move was at the 0 board
           |   |  
        ---+---+---
           | X |  
        ---+---+---
           |   |  
        >>> result.move
        (0, 1, 1)

        >>> notakto.move(0, 0, 1)
        Result(b^1, 0, 0, 1)

    Parameters
    ----------
    boards : list of list of list of int
        A list of 3 x 3 boards ( 0 -> empty, 1 -> occupied )

    Attributes
    ----------
    boards : list of list of list of int
        A list of 3 x 3 boards ( 0 -> empty, 1 -> occupied )
    status : Monoid Class
        the current game status
    """

    def __init__(self, boards):
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

    def is_finish(self):
        for board in self.boards:
            if not self._has_line(board):
                return False
        return True

    def move_check(self, index, x, y):
        if self._is_invalid(index, x, y):
            raise InvalidMoveError
        if self._is_occupied(index, x, y):
            raise GridOccupiedError
        if self._is_dead_board(index):
            raise DeadBoardError

    def move(self, index, x, y, virtual = False):
        self.move_check(index, x, y)
        self.boards[index][x][y] = 1
        status = self.status
        if virtual: self.boards[index][x][y] = 0
        return Result(status, index, x, y)

    def move_random(self, virtual = False):
        index = random.randrange(0, len(self.boards))
        x = random.randrange(0, BOARD_WIDTH)
        y = random.randrange(0, BOARD_WIDTH)
        for _ in range(len(self.boards) * 9):
            try:
                result = self.move(index, x, y, virtual)
                return result
            except DeadBoardError:
                index, x, y = (index + 1) % len(self.boards), 0, 0
            except NotaktoError:
                index, x, y = self._next_index(index, x, y)
        raise NoAvailableMoveError

    def move_optimize(self, virtual = False):
        for k in range(len(self.boards)):
            for i in range(BOARD_WIDTH):
                for j in range(BOARD_WIDTH):
                    try:
                        if self.move(k, i, j, virtual = True).status.is_win():
                            result = self.move(k, i, j, virtual)
                            return result
                    except NotaktoError:
                        pass
        result = self.move_random(virtual)
        return result
