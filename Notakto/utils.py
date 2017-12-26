def board_to_int(board):
    text = ''.join(map(lambda x: ''.join(map(str, x)), board))
    return int(text, 2)
