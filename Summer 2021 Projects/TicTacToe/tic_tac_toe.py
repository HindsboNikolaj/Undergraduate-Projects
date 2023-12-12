# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 23:34:53 2021
Tic Tac Toe Game
@author: nikol
"""
import random
import numpy as np
import copy
"""
initializes the board for a new game.
"""
def init_board():
    board = [0, 0, 0,
             0, 0, 0,
             0, 0, 0]
    return board

""" 
Finds all possible moves given the board and returns all possible moves avaiable.
"""
def all_moves(board):
    moves = []
    for i in range(len(board)):
        if board[i] == 0:
            moves.append(i)
    return moves

"""
Checks if there is a winner on the board, and returns the number of the winner
if there is a winner, -1 if there is no winner but not a tie, and 0 if it is a tie.
"""
def check_winner(board):
    # Check left --> right or up --> down wins
    for i in range(3): 
        if 0 != board[i] == board[i+3] == board[i+6]: # Check down up
            return board[i]
        elif 0 != board[i*3] == board [(i*3)+1] == board[(i*3)+2]:# Left right
            return board[i*3]
    # Check sideways wins
    if 0 != board[0] == board[4] == board[8]: # Upper left corner
        return board[0]
    if 0 != board[2] == board[4] == board[6]: # Upper right corner
        return board[2]
    # No win if at this point
    if 0 in board:
        return -1
    else:
        return 0

"""
Prints tic tac toe board
"""
def check_done(board):
    winner = check_winner(board)
    if winner == -1 or winner == 0:
        return True
    return False

def print_board(board):
    for i in range(3):
        print('|', board[i*3], '|', board[i*3+1], '|', board[i*3+2], '|')
        if i != 2:
            print('-------------')

"""
Performs move, and adds it to the board.
"""
def make_move(board, move, player_number):
    temp = copy.deepcopy(board)
    temp[move] = player_number
    return temp

"""
Picks a random move from the board
"""
def make_random_move(board, player_number):
    moves = all_moves(board)
    move_choice = random.choice(moves)
    board[move_choice] = player_number
    return board, move_choice
    
"""
Main play game function.
"""
def play_game(p1 = None, p2 = None, store_data = False, board = None):
    done = False
    if board is None:
        board = init_board() # Make new game
    curr_board = copy_board(board)
    i = 0
    board_history = None
    if store_data is True:
        board_history = []
        reward = 0
        action = 0
        curr_env_list = [board, action, reward, board, done] # s, a, r, s', done
    while not done: # Play game
        if i % 2 == 0:
            #p1 make move
            if p1 is None: # random player
                action = make_random_move(board, 1)
            else: # if not a random player
                pass
        else:
            #p2 make move
            if p2 is None: # random player
                action = make_random_move(board, 2)
            else: # If not a random player
                pass
        # Now that player has made a move, add to history if storing        
        if check_winner(board) != -1:
            done = True
            winner = check_winner(board)
            # Currently training "X".
            reward = winner
            if winner == 2: # O wins
                reward = -1 # change to negative score
            elif winner == 0: # Tie
                reward = 0.5 # change to 0.5 score
            # loop through history to change reward
        if store_data: # If you want to store data
            curr_env_list = [curr_board, action, reward, board, done]
            board_history.append(curr_env_list)
            curr_board = board
        i += 1 # changes who makes the move.
    #print_board(board)
    if store_data:
        for i in range(len(board_history)):
            board_history[i][2] = reward
            board_history[i] = tuple(board_history[i])
    #print(board_history)
    if store_data:
        return winner, done, board_history
    return winner, done
        
def deep_copy_board_input(board):
    new_board = np.zeros(18)
    for i in range(len(board)):
        if board[i] != 0:
            if board[i] == 1:
                new_board[i] = 1 # List of X's
            else:
                new_board[i+9] = 1 # List of O's
    return new_board     
    
def copy_board(board):
    new_board = []
    for i in range(len(board)):
        new_board.append(board[i])
    return new_board

board = init_board()
#board[0:3] = [2, 2, 2]
#deep_copy_board_input(board)
#print_board(board)
possible_wins = {'1': 0, '2': 0, '0': 0}
play_game(store_data = True)
for i in range(100000):  
    wins = play_game()[0]
    total_wins = possible_wins[str(wins)] + 1
    possible_wins[str(wins)] = total_wins
print(possible_wins)  
print("1 = tie, 2 = nn win, 0 = loss")
print(play_game())
