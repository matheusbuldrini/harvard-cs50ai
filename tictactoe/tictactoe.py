"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None

INF = 9999

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1
    if(count_o < count_x):
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    act = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                act.add((i,j))
    return act


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_boad = deepcopy(board)
    if new_boad[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid Action")    
    new_boad[action[0]][action[1]] = player(board)
    return new_boad


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check lines
    for i in range(3):
        if board[i][0] != EMPTY and board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return board[i][0]
        
    # check columns
    for j in range(3):
        if board[0][j] != EMPTY and board[0][j] == board[1][j] and board[0][j] == board[2][j]:
            return board[0][j]
        
    # check diagonals 
    if board[0][0] != EMPTY and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
            return board[0][0]  
    if board[0][2] != EMPTY and board[0][2] == board[1][1] and board[0][2] == board[2][0]:
            return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return len(actions(board)) == 0 or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def max_value(board):
    if(terminal(board)):
        return (utility(board), None)
    v = -INF
    best_act = None
    for action in actions(board):
        v2 = min_value(result(board, action))[0]
        if v2 > v:
            v = v2
            best_act = action # save action that max player should take
    return (v, best_act)

def min_value(board):
    if(terminal(board)):
        return (utility(board), None)
    v = INF
    best_act = None
    for action in actions(board):
        v2 = max_value(result(board, action))[0]
        if v2 < v:
            v = v2
            best_act = action # save action that min player should take
    return (v, best_act)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # X is maximizing player
    if player(board) == X:
        return max_value(board)[1]
        
    # O is minimizing player
    if player(board) == O:
        return min_value(board)[1]
