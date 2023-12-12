import pygame
import random
import copy
from chess_game.pieces import Pawn
from chess_game.pieces import Bishop
from chess_game.pieces import Knight
from chess_game.pieces import Rook
from chess_game.pieces import Queen
from chess_game.pieces import King
import numpy as np

img_factor = 128
rows, cols = (8, 8)
board = [[None] * cols]*rows

# redraws the board
def redraw(game_board):
    for i in range(8):
        for j in range(8):
             #If it is an even row
            if i%2 == 0:
                    # even row, even column = white
                if j%2 == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (j*img_factor, i*img_factor, img_factor, img_factor))
                    # even row, odd column = brown
                else:
                    pygame.draw.rect(screen, (102, 51, 0), (j * img_factor, i * img_factor, img_factor, img_factor))

            else:# odd row, even column = brown
                if j%2 == 0:
                    pygame.draw.rect(screen, (102, 51, 0), (j * img_factor, i * img_factor, img_factor, img_factor))
                    # odd row, odd column = white
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (j*img_factor, i*img_factor, img_factor, img_factor))
            if game_board[i][j] != None: # If there is a piece on that board, draw it as well.
                game_board[i][j].draw()

    labels = '12345678abcdefgh'

    for i in range(2):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 25)
        for j in range(8):
            if i % 2 == 1:
                text = font.render(labels[j * i], 1, (0, 0, 0))
                screen.blit(text, (5, (img_factor * j)))
            elif i%2 == 0:
                text = font.render(labels[8 + j], 1, (0, 0, 0))
                screen.blit(text, (((img_factor * (j + 1)) - 15), 990))

# Initializes board depending on player colour
def initialize_board(board, player_is_white):
    # Initializing all the pieces based on player colour

    black_rooks = [Rook(0, 0, 'Black', screen), Rook(7, 0, 'Black', screen)]
    black_knights = [Knight(1, 0, 'Black', screen), Knight(6, 0, 'Black', screen)]
    black_bishops = [Bishop(2, 0, 'Black', screen), Bishop(5, 0, 'Black', screen)]
    black_queen = Queen(3, 0, 'Black', screen)
    black_king = King(4, 0, 'Black', screen)
    black_pawns = [Pawn(i, 1, 'Black', screen, False) for i in range(8)]

    white_rooks = [Rook(0, 7, 'White', screen), Rook(7, 7, 'White', screen)]
    white_knights = [Knight(1, 7, 'White', screen), Knight(6, 7, 'White', screen)]
    white_bishops = [Bishop(2, 7, 'White', screen), Bishop(5, 7, 'White', screen)]
    white_queen = Queen(3, 7, 'White', screen)
    white_king = King(4, 7, 'White', screen)
    white_pawns = [Pawn(i, 6, 'White', screen, True) for i in range(8)]
    first_row = []
    # Computer is black
    first_row.append(black_rooks[0])
    first_row.append(black_knights[0])
    first_row.append(black_bishops[0])
    first_row.append(black_queen)
    first_row.append(black_king)
    first_row.append(black_bishops[1])
    first_row.append(black_knights[1])
    first_row.append(black_rooks[1])
    board.append(first_row)
    secondRow = []
    for i in range(0, 8):
        secondRow.append(black_pawns[i])

    board.append(secondRow)

    # Middle squares
    for i in range(0, 4):
        new = []
        for j in range(0, 8):
            new.append(None)
        board.append(new)

    thirdRow = []
    for i in range(0, 8):
        thirdRow.append(white_pawns[i])

    board.append(thirdRow)

    # White (player) Pieces
    fourthRow = []
    fourthRow.append(white_rooks[0])
    fourthRow.append(white_knights[0])
    fourthRow.append(white_bishops[0])
    fourthRow.append(white_queen)
    fourthRow.append(white_king)
    fourthRow.append(white_bishops[1])
    fourthRow.append(white_knights[1])
    fourthRow.append(white_rooks[1])

    board.append(fourthRow)
    return board

"""
Function should be passed a theoretical new board based on their move that just tried to make.
Checks if the ai or the player's king is in check given a board and based on who just made a move.
If the person that just made a move is still in check, that move should not be allowed, and the function should return True
-----------------------------------------
vars:
board - 2D list with theoretical new board with updated move that the person made
player_turn - boolean that shows if it is the player's turn or ai's turn
-----------------------------------------
returns: True if the person that just moved is in check, false otherwise.
"""

def king_in_check(board, player_turn):
    check_found = True
    checks_found = 0
    opponent_color = "Black"
    if player_turn is False:
        opponent_color = "White"


    # First, find the coordinates of the king.
    for row in board:
        for piece in row:
            if piece is not None: # Valid piece
                if piece.type == "King" and opponent_color != piece.color: # Searching for player's king
                    coordinates = [piece.x, piece.y] # List of coordinates
    # Then, check all possible moves of the opponent pieces.
    for row in board:
        for piece in row:
            if piece is not None:
                if piece.color == opponent_color: # Going to check all possible moves of enemy pieces to see if it contains the square of the king

                    if piece.display_moves(board) != [] and coordinates in piece.display_moves(board):
                        print(piece.display_moves(board))
                        print(coordinates in piece.display_moves(board))
                        print(piece.y, piece.x)
                        checks_found += 1
                        check_found = True
    if check_found is True:
        print("Checks Found: ", checks_found)
        return True
    else:
        return False

# Initializing the game
background_colour = (255,255,255)
(width, height) = (img_factor*8, img_factor*8)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess')
screen.fill(background_colour)
pygame.display.flip()
running = True

x_pos = 0
y_pos = 0
for i in range(8):
    x_pos = 0
    for j in range(4):
        if i % 2 == 0:
            x_pos += img_factor
            pygame.draw.rect(screen, (102, 51, 0), (y_pos, x_pos, img_factor, img_factor))
        else:
            pygame.draw.rect(screen, (102, 51, 0), (y_pos, x_pos, img_factor, img_factor))
            x_pos += img_factor
        x_pos += img_factor
    y_pos += img_factor

labels = '12345678abcdefgh'

for i in range(2):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 25)
    for j in range(8):
        if i % 2 == 1:
            text = font.render(labels[j * i], 1, (0,0,0))
            screen.blit(text, (5, (img_factor*j)))
        else:
            text = font.render(labels[8 + j], 1, (0, 0, 0))
            screen.blit(text, (((img_factor * (j+1)) - 15), 990))

# order = Rook:0, Knight:1, Bishop:2, Queen:3, King:4, Bishop:5, Knight:6, Rook:7
# order 2 = Pawn 0:7

# Making the player white or black based on random assignment
random_chance = random.randrange(10) # Random numbers 0-9
# Player will always be on the bottom
if random_chance < 4:
    player_is_white = True
else:
    player_is_white = False

#Black Pieces
board = []
board = initialize_board(board, player_is_white)


clicks = 0
action_done = False
current_piece = None
player_turn = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_pos, y_pos = pygame.mouse.get_pos()
            x_pos //= 128
            y_pos //= 128
            if clicks == 1:
                if(current_piece.isValidMove(x_pos, y_pos, possibleMoves) and ((player_turn is True and board[prev_y][prev_x].color == "White") or (player_turn is False and board[prev_y][prev_x].color == "Black"))):
                    board[y_pos][x_pos] = current_piece
                    board[current_piece.y][current_piece.x] = None
                    current_piece.x = x_pos
                    current_piece.y = y_pos
                    king_in_check(board, player_turn)
                    if player_turn is True:
                        player_turn = False
                    else:
                        player_turn = True
                clicks = 0
                redraw(board)
                action_done = True

            if clicks == 0 and action_done == False and board[y_pos][x_pos] is not None and ((player_turn is True and board[y_pos][x_pos].color == "White") or (player_turn is False and board[y_pos][x_pos].color == "Black")):
                if(board[y_pos][x_pos] != None):
                    current_piece = board[y_pos][x_pos]
                    possibleMoves = current_piece.display_moves(board)
                    clicks+=1
                    prev_x =x_pos
                    prev_y = y_pos


            action_done = False











    pygame.display.update()