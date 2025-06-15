"""
Tic Tac Toe Player
"""

import math    
import copy

X = "X"
O = "O"
EMPTY = None

# Initial configuration


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Choice of the player


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_elements = sum(row.count(X) for row in board)
    o_elements = sum(row.count(O) for row in board)
    if x_elements == o_elements:
        return X
    else:
        return O

# In which empty space can the player input his choice 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    list_possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                list_possible_actions.add((i, j))
    return list_possible_actions

# The resulting state from the previous action 


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid Action")
    
    new_state = copy.deepcopy(board)
    new_state[action[0]][action[1]] = player(board)
    return new_state

# Defines the winning conditions


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][0] == board[2][0] and board[0][0] is not EMPTY:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] and board[0][1] is not EMPTY:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] and board[0][2] is not EMPTY:
        return board[0][2]
    elif board[0][0] == board[0][1] == board[0][2] and board[0][0] is not EMPTY:
        return board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] and board[1][0] is not EMPTY:
        return board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] and board[2][0] is not EMPTY:
        return board[2][0]
    elif board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    elif board[2][0] == board[1][1] == board[0][2] and board[2][0] is not EMPTY:
        return board[2][0]
    else:
        return None

# Decides the Game Over


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not actions(board)

# Gives a numerical value to the end game (1 for an X win, -1 for a O win, 0 for a tie)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

# Main algorithm for the AI choice


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        
        if terminal(board):
            return utility(board), EMPTY
        
        optm = float('-inf')
        for k in actions(board):
            current_optm = max(optm, min_value(result(board, k))[0])
            if current_optm > optm:
                optm_action = k
                optm = current_optm
        return optm, optm_action
    
    def min_value(board):
        
        if terminal(board):
            return utility(board), EMPTY
        
        optm = float('inf')
        for k in actions(board):
            current_optm = min(optm, max_value(result(board, k))[0])
            if current_optm < optm:
                optm_action = k
                optm = current_optm
        return optm, optm_action
    
    player_state = player(board)
    
    if terminal(board):
        return None
    
    if player_state == X:
        return max_value(board)[1]
    elif player_state == O:
        return min_value(board)[1]