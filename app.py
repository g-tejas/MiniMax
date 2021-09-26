'''
TIC TAC TOE ALGORITHM FROM SCRATCH
USING MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING

using Tkinter
'''

# Import all the necessary dependencies
import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
import numpy as np

# Sign variable to decide whose turn it is (Computer or Player)
sign = 0

# Creates an empty board
global board
board = [[" " for x in range(3)] for y in range(3)]

# Check if anyone has won the game given a state of the board
def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0] # Return the first element since they're all the same
    return 0 # if there is no winner

def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0] # Since its the left to right diagonal, return the first element
    if len(set([board[i][len(board)-1-i] for i in range(len(board))])) == 1:
        return board[0][len(board)-1] # Right to left diagonal
    return 0 # if there is no winner

def returnWinner(board):
    # Check the rows/columns by transposing the board
    for b in [board, np.transpose(board)]:
        result = checkRows(b)
        if result: # Integer 0 is considered a false bool
            return result
    # Check the diagonals
    # Don't need a for loop, because this function checks all combinations, unlike the rows one
    return checkDiagonals(board)

a = [['X', '', 'A'],
     ['A', 'X', 'A'],
     ['A', '', 'X']]

print(returnWinner(a))