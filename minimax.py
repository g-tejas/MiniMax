from math import inf as infinity
from time import sleep
import os
import numpy as np
from random import choice

COMP = +1
HUMAN = -1
count = 0

def generate_board():
    return [[0 for _ in range(3)] for _ in range(3)]

def render(state):
    chars = {
        -1: 'O', # human
        +1: 'X', # computer
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)

def index_to_coord(index):
    row, col = divmod(index-1,3)
    return [row,col]

def checkWinner(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):
    return checkWinner(state, HUMAN) or checkWinner(state, COMP) or len(empty_cells(state)) == 0

def evaluate(state):
    # since evaluate() will only be called on a game when it's over, there's no need to 
    # put another if statement
    if checkWinner(state, COMP):
        score = +10
    elif checkWinner(state, HUMAN):
        score = -10
    else:
        score = 0
        
    return score

def empty_cells(state):
    empty_cells = []
    for i in range(10):
        if i != 0:
            row, col = divmod(i - 1, 3)
            if state[row][col] == 0:
                empty_cells.append(i)
    return empty_cells

def valid_move(state, position):
    if position in empty_cells(state):
        return True
    else:
        return False

def place_move(state, position, player):
    if valid_move(state, position):
        coord = index_to_coord(position)
        state[coord[0]][coord[1]] = player
        return True
    return False

def undo_move(state, position):
    row, col = divmod(position-1, 3)
    state[row][col] = 0
    return True

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def minimax(state, depth, isMaximizer):
    global count
    if game_over(state):
        count += 1
        score = evaluate(state)
        if score != 0:
            if checkWinner(state, COMP):
                score = score - depth
            elif checkWinner(state, HUMAN):
                score = score + depth
        return score
    
    if isMaximizer: # the ai's turn
        maxEval = -infinity
        bestPosition = choice(empty_cells(state))
        for position in empty_cells(state):
            place_move(state, position, COMP)
            eval = minimax(state, depth + 1, False)
            undo_move(state, position)
            if eval > maxEval:
                maxEval = eval
                bestPosition = position
        if depth == 0:
            print(f"Searched {count} possible end states without pruning")
            return bestPosition
        return maxEval
    
    else:
        minEval = infinity
        for position in empty_cells(state):
            place_move(state, position, HUMAN)
            eval = minimax(state, depth + 1, True)
            undo_move(state, position)
            if eval < minEval:
                minEval = eval
        return minEval


def ai_turn(state):
    if game_over(state):
        return
    
    clean()
    print("Computer's turn [X]") # header
    render(state) # Print current board to show the human what are his options

    
    if len(empty_cells(state)) == 9: # if the board is not empty
        move = choice(range(0,9)) # if the board is empty
    else:
        move = minimax(state, 0, True)
    
    place_move(state, move, COMP)
    sleep(1)  

def human_turn(state):
    if game_over(state):
        return
    
    clean()
    print("Human's turn [O]") # header
    render(state) # Print current board to show the human what are his options

    move = -1 # input invalid move index

    # Keep asking him to enter his move choice until its a valid move
    while move < 1 or move > 9:
        try:
            move = int(input('Enter your position from 1-9:'))
            can_move = place_move(state, move, HUMAN)
            if not can_move:
                print('Invalid move')
                move = -1 # Need him to enter a correct move
        except(EOFError, KeyboardInterrupt):
            print("Bye")
            exit()
        except(KeyError, ValueError): # if they input some funny number
            print("Please enter only numeric values.")

def main():
    
    clean()
    humanFirst = "" # whether the human starts first or not

    board = generate_board() # create an empty board

    while humanFirst != "Y" and humanFirst != "N": # while 
        try:
            humanFirst = input("Would you like to go first? \n[Y/N]: ").upper()
        except(EOFError, KeyboardInterrupt):
            print("Bye bye")
            exit()
        except(KeyError, ValueError):
            print("Y or N only please")
    
    # Main loop of the game
    while not game_over(board):
        if humanFirst == "N":
            ai_turn(board)
            humanFirst = "Y" # so it wont execute this block again

        human_turn(board)
        ai_turn(board)

    # Game over message
    if checkWinner(board, COMP):
        clean()
        render(board)
        print("YOU LOST!")
    elif checkWinner(board, HUMAN):
        clean()
        render(board)
        print("YOU WON!")
    else:
        clean()
        render(board)
        print("IT'S A DRAW!")

    exit()

if __name__ == "__main__":
    main()