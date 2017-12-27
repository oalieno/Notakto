def board_to_int(board):
    text = ''.join(map(lambda x: ''.join(map(str, x)), board))
    return int(text, 2)

def int_to_board(num):
    binary = list(map(int, "{:09b}".format(num)))
    return [[binary[0], binary[1], binary[2]],
            [binary[3], binary[4], binary[5]],
            [binary[6], binary[7], binary[8]]]

def empty_board():
    return int_to_board(0)
