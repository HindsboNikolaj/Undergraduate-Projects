# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 18:38:19 2021
Main Class for Chess Game
This will contain chess information.
@author: Nikolaj Hindsbo

credit for some inspiration: sunfish gh: thomasahle
"""

##############################################################################
### Piece                                                               
### Capital letters - Black                                                 
### 'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟'               
###  Non-capital letters - White                                            
### 'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.' empty    
##############################################################################


##############################################################################
### CONSTANTS
##############################################################################

# Corner pieces to detect valid moves
A1, H1, A8, H8 = 91, 98, 21, 28 # Valid moves must end in 1-8, begins through 21-98

# Board represented as a 120 character string. 
# Allows for padding and check for valid moves

starting_board = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' rnbqkbnr\n'  #  20 - 29
    ' pppppppp\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' PPPPPPPP\n'  #  80 - 89
    ' RNBQKBNR\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
)

# Possible moves for each type
N, W, E, S = -10, -1, 1, 10

# Dictionary of direction of moves that the pieces can travel

direction_dict = {
    'P': (N, N+N, N+W, N+E),
    'R': (N, W, E, S),
    'N': (N+N+W, N+N+E, S+S+W, S+S+E, S+E+E, S+W+W, N+W+W, N+E+E),
    'B': (N+E, N+W, S+E, S+W),
    'Q': (N, W, E, S, N+E, N+W, S+E, S+W),
    'K': (N, W, E, S, N+E, N+W, S+E, S+W)
}

move_dict = {
    'a': 2,
    'b': 3,
    'c': 4,
    'd': 5,
    'e': 6,
    'f': 7,
    'g': 8,
    'h': 9,
    '1': 9,
    '2': 8,
    '3': 7,
    '4': 6,
    '5': 5,
    '6': 4,
    '7': 3,
    '8': 2
}

# Minimum and maximum score for mate, upper given
# by mate in 1, and lower given by mate in (max depth)..
# If for some reason that is lower, will just use MATE_LOWER.

MATE_LOWER = 0
MATE_UPPER = 0

# Table size - max # elements ** TUNE**
TABLE_SIZE = 1e7

# Constants for search
QS_SEARCH = 219 # Quiescence Search
EVAL_ROUGHNESS = 13 # **TUNE**
DRAW_TEST = True


##############################################################################
### BOARD FUNCTIONS
##############################################################################
"""
draw_board draws the chess board in the console.

@parameters
board - a 120 character string represented as the board.
@returns - none, prints board on console
"""
def draw_board(board):
    for i, row in enumerate(board.split()):
        print(' ', 8-i, ' ', " ".join(row))
    print('\n      a b c d e f g h \n\n')

"""
move_board moves the piece that user input has tried to move.
checks if valid input is given, and if the move is legal.
@parameters
board - a 120 character string represented as the board.
move - a four character string representing piece they want to move & where ex: f1g1
@returns - True if move can be done, False otherwise. Also returns new board after that move is done.
"""
def move_piece(board, move):
    valid_move = False
    new_board = board
    # Check for valid input
    if not move_input_is_valid(move)[0]:
        return False, move_input_is_valid(move)[1]
    # Check for valid move
    elif not move_is_legal(board, move):
        pass
    
    
    return valid_move, new_board

"""
Checks if valid move input is given, represented as a move from-to.
Does not check if move is legal, or if there is actually a piece to be moved.
@parameters
move - a four character string representing piece that they want to move & where
@returns - True if move is valid, false otherwise with message why it is false.
"""
def move_input_is_valid(move):
    # Check length of move is 4
    if len(move) != 4:
        return False
    # Check that each part is valid alphabet/number
    i = 0
    for char in move:
        if i % 2 == 0:
            if char.isalpha():
                if not ('a' <= char <= 'h'): # Not between a-h
                    return False, "Incorrect placement. Try something like Try something like: a1b2"
            else:
                return False, "Incorrect placement. Try something like Try something like: a1b2"
        else:
            if char.isalpha():
                return False, "Incorrect placement. Try something like Try something like: a1b2"
            else:
                if not('1' <= char <= '8'): # Not between 1-8
                    return False, "Incorrect placement. Try something like Try something like: a1b2"
        i += 1
    # Now check that dosen't just move to same spot
    if move[0:2] == move[2:4]:
        return False, "Cannot move to and from the same spot. Try something like: a1b2"
    return True, ""
                
        
"""
Checks if a move is legal, given the board.
@parameters
board - a 120 character string represented as the board
move - a four character string representing piece that they want to move & where.
    (assumed to be valid, maybe not legal).
@returns - True if move is legal, false otherwise.
"""
def move_is_legal(board, move, player_is_white):
    
    # First, check if the board has the correct color piece on original move
    original = move_dict[move[1]]*10 + move_dict[move[0]]
    to = move_dict[move[3]]*10 + move_dict[move[2]]
    if board[original] == ".":
        pass
    
draw_board(starting_board)

