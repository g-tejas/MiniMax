from minimax import minimax
from math import inf

board = [
    [1,0,0],
    [0,0,0],
    [0,0,0]
]

result = minimax(board, 0, -inf, inf, True)