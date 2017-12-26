class NotaktoError(Exception):
    pass

class InvalidMoveError(NotaktoError):
    pass

class GridOccupiedError(NotaktoError):
    pass

class DeadBoardError(NotaktoError):
    pass

class NoAvailableMoveError(NotaktoError):
    pass
