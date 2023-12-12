# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 17:26:37 2021

@author: nikol
"""
import math
import tic_tac_toe as ttt
X_VALUE = 1
O_VALUE = 2
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

"""
create a min-max player for tic-tac-toe.
Default value of min-max is 2 (they are the O-player), 1 for player (X).
This class will just rationalize which min-max it is searching for.
"""

class min_max_player():
    
    """ 
    Initialize the class, and initialize if player is X or O.
    """
    
    def __init__(self, ai_is_x = True):
        self.ai_num = 1
        self.player_num = 2
        if ai_is_x is False:
            self.ai_num = 2
            self.player_num = 1
        
            
    """
    TO BE DELETED *****
    """
            
    def test_regression(self, board, num):
        print(board, num)
        board[0] = 4
        if num == 1:
            self.test_regression(board, 2)
        board[0] = 0
        print(board, num)
    
    """
    
    returns the best move and the best possible score for the state in an array
    format [move, score]
    """
    
    def min_max(self, board, depth, ai_turn = True):
        pass
        if ai_turn: # Ai is max
            move_num = self.ai_num
            best = [-1, -float('inf')]
        else: # Player is min
            move_num = self.player_num
            best = [-1, float('inf')]
            
        board_reward = self.check_winner(board)
        if board_reward != -1 or depth == 0: # If the game is over.
            if ai_turn is False:
                if board_reward == self.player_num:
                    return [-1, -1]
            return [-1, board_reward]
        
        # Otherwise, we need to run out min-max algorithm.
        all_moves = self.all_moves(board)
        for move in all_moves:
            if ai_turn:
                board[move] = self.ai_num
            else:
                board[move] = self.player_num
            
            new_move, move_score = self.min_max(board, depth-1, not ai_turn)
            board[move] = 0
            print(board, move_score)
            if ai_turn: # Check if move_score is better than current best for ai
                if move_score > best[1]: # Move is new best
                    best = [move, move_score]
            else: # Check if move_score is better than current best for player
                if move_score < best[1]:
                    best = [move, move_score]
        return best
    
    """
    check the winner of the board.
    returns None if there is no winner, '1' if X wins, '2' if O wins,  
    '0' if there is a tie, -1 if no winner yet.
    """
    
    def check_winner(self, board):
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
    returns all moves possbile for that board in a list format.
    """
    def all_moves(self, board):
        possible_moves = []
        for i in range(len(board)):
            if board[i] == 0:
                possible_moves.append(i)
        return possible_moves
        
        
    
test_ai = min_max_player()
test_ai.test_regression(board, 1)
board[1] = 2
board[2] = 1
board[5] = 1
board[4] = 2
move, score = test_ai.min_max(board, len(test_ai.all_moves(board)), ai_turn = True)
print(move, score)
ttt.print_board(board)
        
    
    
    