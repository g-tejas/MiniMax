import numpy as np

def convert_input(x):
    if x == 1:
        return (0,0)
    elif x == 2:
        return (0,1)
    elif x == 3:
        return (0,2)
    elif x == 4:
        return (1,0)
    elif x == 5:
        return (1,1)
    elif x == 6:
        return (1,2)
    elif x == 7:
        return (2,0)
    elif x == 8:
        return (2,1)
    elif x == 9:
        return (2,2)

def welcome_msg():
    print("Computer goes first! Good luck!\n Positions are as follow:\n")
    print(
        '1, 2, 3\n',
        '4, 5, 6\n',
        '7, 8, 9\n'
    )


def checkWinner(state):
    for board in [state, np.transpose(state)]:
        for row in board:
            if len(set(row)) == 1 and row[0] != 0:
                return True

    if len(set([state[i][i] for i in range(len(state))])) == 1 and state[0][0] != 0:
        return True

    if len(set([state[i][len(state)-1-i] for i in range(len(state))])) == 1 and state[0][2] != 0:
        return True
    
    return False


def empty_cells(state):
    '''
    Description:
        - Given the state of a board, returns a list containing the coordinates of the
        cells that are empty

    Arguments:
        - state; list of lists

    Returns:
        - empty_list; list of tuples
    '''
    empty_list = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                empty_list.append((i,j)) # Append the coordinates to the list
    return empty_list # returns a tuple

def checkDraw(state):
    if checkWinner(state) == False and len(empty_cells(state)) == 0:
        return True # if its a draws
    else:
        return False
        
def place_move(player, state, position):
    if position in empty_cells(state): # if the cell is empty
        state[position[0]][position[1]] = player # place the move
        render(state) # render the board

        if checkDraw(state):
            print("Draw!")
            exit()
        
        result = checkWinner(state) # check if anyone won
        if result != False:
            if result == 1:
                print("Human has won")
                exit()
            else:
                print("Computer has won")
                exit()
        return

    else:
        print("Invalid position")
        position = tuple(map(
                    int, input('Please enter your move coordinates: \n').split(',')
                ))
        place_move(player, state, position)
        return

def human_turn(state):
    coordinates = tuple(map(
                int, input('Please enter your move coordinates: \n').split(',')
            ))
    place_move(1, state, coordinates)
    return

def minimax(state, depth, maximizingPlayer):
    '''
    Arguments:
        - state = List of lists, Current state of the board
        - depth = Int, How far ahead do you want the bot to see
        - maximizingPlayer = bool, whether it is the maximising player's turn or not
    
    Returns:
        - The best score.
    '''
    if checkWinner(state) == False:
        if checkDraw(state) == True:
            return 0
    else:
        return checkWinner(state)

    if maximizingPlayer:
        maxEval = float('-inf')

        for position in empty_cells(state):
            # Make the move
            state[position[0]][position[1]] = -1  # Since it's the bot playing to win
            eval = minimax(state, depth+1, False)
            maxEval = max(eval, maxEval)
            # undo the move
            state[position[0]][position[1]] = 0
        return maxEval
    
    else: # if it's the minimisers turn
        minEval = float('inf')

        for position in empty_cells(state):
            # Make the move
            state[position[0]][position[1]] = 1  # Since it's the bot playing to win
            eval = minimax(state, depth+1, True)
            minEval = min(eval, minEval)
            # undo the move
            state[position[0]][position[1]] = 0
        return minEval

def ai_turn(state):
    maxEval = float('-inf')
    best_move = (-1,-1)

    for position in empty_cells(state):
        state[position[0]][position[1]] == -1 # Place the move on every possible child

        eval = minimax(state, 0, False) # maximizing player is False because it's the humans turn

        state[position[0]][position[1]] == 0

        if eval > maxEval:
            best_move = position
            maxEval = eval
    
    place_move(-1, state, best_move)
    return
