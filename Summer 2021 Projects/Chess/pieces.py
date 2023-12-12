import numpy as np
import pygame

imgFactor = 128
# Overall, not bad but WTF why did i write the x and y this way???? >>>> tilt.

class Pieces():

    def __init__(self, x, y, type, color, screen):
        self.x = x
        self.y = y
        self.type = type
        self.screen = screen
        self.color = color
        self.draw()

    def draw(self):
        image = pygame.image.load(self.type + self.color + '.png')
        image = pygame.transform.scale(image, (imgFactor, imgFactor))
        self.screen.blit(image, (self.x * imgFactor + (imgFactor / 2 - image.get_width() / 2)
                                 , self.y * imgFactor + (imgFactor / 2 - image.get_height() / 2)))

    def draw_circle(self, x, y, board):
        if board[y][x] == None:
            pygame.draw.circle(self.screen, (0, 0, 0)
                               , ((int)(x * imgFactor + imgFactor / 2), (int)(y * imgFactor + imgFactor / 2)), 15, 1)
        else:
            pygame.draw.circle(self.screen, (255, 0, 0)
                               , ((int)(x * imgFactor + imgFactor / 2), (int)(y * imgFactor + imgFactor / 2)), 15, 1)

    def isValidMove(self, x, y, arrPossible):
        if (arrPossible is None):
            return False
        isValid = False
        for i in range(len(arrPossible)):
            if (arrPossible[i][0] == x and arrPossible[i][1] == y):
                isValid = True
                i = len(arrPossible) - 1
                self.hasMoved = True
        return isValid

#TODO - FIX - TRY TO MAKE IT VERSATILE???? fuck this is stupid.
class Pawn(Pieces):
    def __init__(self, x, y, color, screen, upper_is_black):
        super().__init__(x, y, "Pawn", color, screen)
        self.hasMoved = False
        self.upper_is_black = upper_is_black

    # Displays the possible moves for the selected pawn.
    def display_moves(self, board):
        if self.upper_is_black:
            return self.display_up_move(board)
        else:
            return self.display_down_move(board)

    def display_up_move(self, board):
        # Possible move 2-forward if never moved before
        arr = []

        if not self.hasMoved and board[self.y - 2][self.x] == None and board[self.y - 1][self.x] == None:
            self.draw_circle(self.x, self.y - 1, board)
            self.draw_circle(self.x, self.y - 2, board)
            arr.append([self.x, self.y - 1])
            arr.append([self.x, self.y - 2])

        # Possible 1-foward move if it has moved before
        if self.y > 0:
            if self.hasMoved and board[self.y - 1][self.x] == None:
                self.draw_circle(self.x, self.y - 1, board)
                arr.append([self.x, self.y - 1])

        # Possible take to the right
        if self.x < 7 and self.y > 0:
            if board[self.y - 1][self.x + 1] != None and self.color != board[self.y - 1][self.x + 1].color:
                self.draw_circle(self.x + 1, self.y - 1, board)
                arr.append([self.x + 1, self.y - 1])

        # Possible take to the left
        if self.x > 0 and self.y > 0:
            if board[self.y - 1][self.x - 1] != None and self.color != board[self.y - 1][self.x - 1].color:
                self.draw_circle(self.x - 1, self.y - 1, board)
                arr.append([self.x - 1, self.y - 1])
        return arr

    def display_down_move(self, board):
        arr = []
        if not self.hasMoved and board[self.y + 1][self.x] == None:
            self.draw_circle(self.x, self.y + 1, board)
            arr.append([self.x, self.y + 1])
            if board[self.y + 2][self.x] == None:
                self.draw_circle(self.x, self.y + 2, board)
                arr.append([self.x, self.y + 2])

        # Possible 1-foward move if it has moved before
        if self.y > 0:
            if self.hasMoved and board[self.y + 1][self.x] == None:
                self.draw_circle(self.x, self.y + 1, board)
                arr.append([self.x, self.y + 1])

        # Possible take to the right
        if self.x < 7 and self.y < 7:
            if board[self.y + 1][self.x + 1] != None and self.color != board[self.y + 1][self.x + 1].color:
                self.draw_circle(self.x + 1, self.y + 1, board)
                arr.append([self.x + 1, self.y + 1])

        # Possible take to the left
        if self.x > 0 and self.y < 7:
            if board[self.y + 1][self.x - 1] != None and board[self.y + 1][self.x - 1].color != self.color:
                self.draw_circle(self.x - 1, self.y + 1, board)
                arr.append([self.x - 1, self.y + 1])

        return arr


class Bishop(Pieces):
    def __init__(self, x, y, color, screen):
        super().__init__(x, y, "Bishop", color, screen)

    def display_moves(self, board):
        arr = []
        leftUp = True
        leftDown = True
        rightUp = True
        rightDown = True

        tempX = self.x
        tempY = self.y

        # checks movement to the left and up
        while leftUp:
            if tempY != 0 and tempX != 0:
                if board[tempY - 1][tempX - 1] == None or board[tempY - 1][tempX - 1].color != self.color:
                    if (board[tempY - 1][tempX - 1] != None):
                        self.draw_circle(tempX - 1, tempY - 1, board)
                        arr.append([tempX - 1, tempY - 1])
                        leftUp = False
                    else:
                        self.draw_circle(tempX - 1, tempY - 1, board)
                        arr.append([tempX - 1, tempY - 1])
                    tempX -= 1
                    tempY -= 1
                else:
                    leftUp = False
            else:
                leftUp = False

        tempX = self.x
        tempY = self.y
        # Checks movement to the left and down
        while (leftDown):
            if (tempY != 7 and tempX != 0 and (board[tempY + 1][tempX - 1] is None or board[tempY + 1][tempX - 1].color != self.color)):
                self.draw_circle(tempX - 1, tempY + 1, board)
                arr.append([tempX - 1, tempY + 1])
                if (board[tempY + 1][tempX - 1] is not None):
                    leftDown = False
                tempX -= 1
                tempY += 1

            else:
                leftDown = False

        tempX = self.x
        tempY = self.y
        #checks movement to the right and up
        while (rightUp):
            if (tempY != 0 and tempX != 7):
                if (board[tempY - 1][tempX + 1] == None or board[tempY - 1][tempX + 1].color != self.color):
                    self.draw_circle(tempX + 1, tempY - 1, board)
                    arr.append([tempX + 1, tempY - 1])
                if (board[tempY - 1][tempX + 1] != None):
                    rightUp = False
                tempX += 1
                tempY -= 1

            else:
                rightUp = False
        tempX = self.x
        tempY = self.y
        #Checks movement to the right and down
        while (rightDown):
            if (tempY != 7 and tempX != 7):
                if(board[tempY +1][tempX +1] is None or board[tempY + 1][tempX +1].color != self.color):
                    self.draw_circle(tempX + 1, tempY + 1, board)
                    arr.append([tempX + 1, tempY + 1])
                if (board[tempY + 1][tempX + 1] != None):
                    rightDown = False
                tempX += 1
                tempY += 1
            else:
                rightDown = False

        return arr


class Knight(Pieces):
    def __init__(self, x, y, color, screen):
        super().__init__(x, y, "Knight", color, screen)

    def display_moves(self, board):

        #check if in bounds
        #check if none, or of a different color.
        arr = []
        #ALL UPWARDS MOTIONS

        #up 2, right 1:
        if(self.x < 7 and self.y > 1):
            #Checks if none, or of a different color:
            if(board[self.y - 2][self.x + 1] == None or board[self.y -2][self.x + 1].color != self.color):
                arr.append([self.x + 1,self.y -2])
                self.draw_circle(self.x + 1, self.y -2, board)

        #right 2, up 1
        if(self.x < 6 and self.y > 0):
            if (board[self.y - 1][self.x + 2] == None or board[self.y - 1][self.x + 2].color != self.color):
                arr.append([self.x + 2, self.y - 1])
                self.draw_circle(self.x + 2, self.y - 1, board)

        #up 2, left 1:
        if(self.x > 0 and self.y > 1):
            if (board[self.y - 2][self.x - 1] == None or board[self.y - 2][self.x - 1].color != self.color):
                arr.append([self.x - 1, self.y - 2])
                self.draw_circle(self.x - 1, self.y - 2, board)

        #left 2, up 1:
        if(self.x > 1 and self.y > 0):
            if (board[self.y - 1][self.x - 2] == None or board[self.y - 1][self.x - 2].color != self.color):
                arr.append([self.x - 2, self.y - 1])
                self.draw_circle(self.x - 2, self.y - 1, board)

        # ALL DOWNWARDS MOTIONS

        #down 2, right 1:
        if(self.x < 7 and self.y < 6):
            # Checks if none, or of a different color:
            if (board[self.y + 2][self.x + 1] == None or board[self.y + 2][self.x + 1].color != self.color):
                arr.append([self.x + 1, self.y + 2])
                self.draw_circle(self.x + 1, self.y + 2, board)
        #right 2, down 1:
        if(self.x < 6 and self.y < 7):
             if (board[self.y + 1][self.x + 2] == None or board[self.y + 1][self.x + 2].color != self.color):
                 arr.append([self.x + 2, self.y  + 1])
                 self.draw_circle(self.x + 2, self.y + 1, board)
        #down 2, left 1:
        if(self.x > 0 and self.y < 6):
            if (board[self.y + 2][self.x - 1] == None or board[self.y + 2][self.x - 1].color != self.color):
                arr.append([self.x - 1, self.y + 2])
                self.draw_circle(self.x - 1, self.y + 2, board)
        #left 2, down 1:
        if(self.x > 1 and self.y < 7):
             if (board[self.y + 1][self.x - 2] == None or board[self.y + 1][self.x - 2].color != self.color):
                arr.append([self.x - 2, self.y + 1])
                self.draw_circle(self.x - 2, self.y + 1, board)
        return arr


class Rook(Pieces):

    def __init__(self, x, y, color, screen):
        super().__init__(x, y, "Rook", color, screen)

    def display_moves(self, board):
        arr = []
        left = True
        right = True
        up = True
        down = True
        tempX = self.x
        tempY = self.y
        while(left):
            if(tempX != 0):
                #left is none
                if(board[tempY][tempX -1] is None):
                    self.draw_circle(tempX -1, tempY, board)
                    arr.append([tempX -1, tempY])
                    tempX -= 1
                #Left is not none, but of the same color
                elif board[tempY][tempX -1].color == self.color:
                    left = False
                #Left is none, and of different color
                else:
                    arr.append([tempX -1, tempY])
                    self.draw_circle(tempX -1, tempY, board)
                    left = False
            else:
                left = False
        tempX = self.x
        tempY = self.y
        while (right):
            if (tempX != 7):
                # Right is none
                if (board[tempY][tempX + 1] is None):
                    self.draw_circle(tempX + 1, tempY, board)
                    arr.append([tempX + 1, tempY])
                    tempX += 1
                # Right is not none, but of the same color
                elif board[tempY][tempX + 1].color == self.color:
                    right = False
                # Right is none, and of different color
                else:
                    self.draw_circle(tempX + 1, tempY, board)
                    arr.append([tempX + 1, tempY])
                    right = False
            else:
                right = False
        tempX = self.x
        tempY = self.y
        while(down):
            if (tempY != 7):
                # Down is none
                if (board[tempY + 1][tempX] is None):
                    self.draw_circle(tempX, tempY + 1, board)
                    arr.append([tempX, tempY + 1])
                    tempY += 1
                # Down is not none, but of the same color
                elif board[tempY + 1][tempX].color == self.color:
                    down = False
                # Down is none, and of different color
                else:
                    self.draw_circle(tempX, tempY + 1, board)
                    arr.append([tempX, tempY + 1])
                    down = False
            else:
                down = False

        tempX = self.x
        tempY = self.y
        while (up):
            if (tempY != 0):
                # Up is none
                if (board[tempY - 1][tempX] is None):
                    self.draw_circle(tempX, tempY - 1, board)
                    arr.append([tempX, tempY - 1])
                    tempY -= 1
                # Up is not none, but of the same color
                elif board[tempY - 1][tempX].color == self.color:
                    up = False
                # Up is none, and of different color
                else:
                    self.draw_circle(tempX, tempY - 1, board)
                    arr.append([tempX, tempY - 1])
                    up = False
            else:
                up = False

        return arr


class Queen(Pieces):
    def __init__(self, x, y, color, screen):
        super().__init__(x, y, "Queen", color, screen)

    def display_moves(self, board):
        arr = []
        arr1 = self.bishopMoves(board)
        arr2 = self.rookMoves(board)
        for i in range(len(arr1)):
            arr.append([arr1[i][0], arr1[i][1]])
        for j in range(len(arr2)):
            arr.append([arr2[j][0], arr2[j][1]])

        return arr
    def bishopMoves(self, board):
        arr = []
        leftUp = True
        leftDown = True
        rightUp = True
        rightDown = True

        tempX = self.x
        tempY = self.y

        # checks movement to the left and up
        while leftUp:
            if tempY != 0 and tempX != 0:
                if board[tempY - 1][tempX - 1] == None or board[tempY - 1][tempX - 1].color != self.color:
                    if (board[tempY - 1][tempX - 1] != None):
                        self.draw_circle(tempX - 1, tempY - 1, board)
                        arr.append([tempX - 1, tempY - 1])
                        leftUp = False
                    else:
                        self.draw_circle(tempX - 1, tempY - 1, board)
                        arr.append([tempX - 1, tempY - 1])
                    tempX -= 1
                    tempY -= 1
                else:
                    leftUp = False
            else:
                leftUp = False

        tempX = self.x
        tempY = self.y
        # Checks movement to the left and down
        while (leftDown):
            if (tempY != 7 and tempX != 0 and (
                    board[tempY + 1][tempX - 1] is None or board[tempY + 1][tempX - 1].color != self.color)):
                self.draw_circle(tempX - 1, tempY + 1, board)
                arr.append([tempX - 1, tempY + 1])
                if (board[tempY + 1][tempX - 1] is not None):
                    leftDown = False
                tempX -= 1
                tempY += 1

            else:
                leftDown = False

        tempX = self.x
        tempY = self.y
        # checks movement to the right and up
        while (rightUp):
            if (tempY != 0 and tempX != 7):
                if (board[tempY - 1][tempX + 1] == None or board[tempY - 1][tempX + 1].color != self.color):
                    self.draw_circle(tempX + 1, tempY - 1, board)
                    arr.append([tempX + 1, tempY - 1])
                if (board[tempY - 1][tempX + 1] != None):
                    rightUp = False
                tempX += 1
                tempY -= 1

            else:
                rightUp = False
        tempX = self.x
        tempY = self.y
        # Checks movement to the right and down
        while (rightDown):
            if (tempY != 7 and tempX != 7):
                if (board[tempY + 1][tempX + 1] is None or board[tempY + 1][tempX + 1].color != self.color):
                    self.draw_circle(tempX + 1, tempY + 1, board)
                    arr.append([tempX + 1, tempY + 1])
                if (board[tempY + 1][tempX + 1] != None):
                    rightDown = False
                tempX += 1
                tempY += 1
            else:
                rightDown = False

        return arr

    def rookMoves(self, board):
        arr = []
        left = True
        right = True
        up = True
        down = True
        tempX = self.x
        tempY = self.y
        while (left):
            if (tempX != 0):
                # left is none
                if (board[tempY][tempX - 1] is None):
                    self.draw_circle(tempX - 1, tempY, board)
                    arr.append([tempX - 1, tempY])
                    tempX -= 1
                # Left is not none, but of the same color
                elif board[tempY][tempX - 1].color == self.color:
                    left = False
                # Left is none, and of different color
                else:
                    arr.append([tempX - 1, tempY])
                    self.draw_circle(tempX - 1, tempY, board)
                    left = False
            else:
                left = False
        tempX = self.x
        tempY = self.y
        while (right):
            if (tempX != 7):
                # Right is none
                if (board[tempY][tempX + 1] is None):
                    self.draw_circle(tempX + 1, tempY, board)
                    arr.append([tempX + 1, tempY])
                    tempX += 1
                # Right is not none, but of the same color
                elif board[tempY][tempX + 1].color == self.color:
                    right = False
                # Right is none, and of different color
                else:
                    self.draw_circle(tempX + 1, tempY, board)
                    arr.append([tempX + 1, tempY])
                    right = False
            else:
                right = False
        tempX = self.x
        tempY = self.y
        while (down):
            if (tempY != 7):
                # Down is none
                if (board[tempY + 1][tempX] is None):
                    self.draw_circle(tempX, tempY + 1, board)
                    arr.append([tempX, tempY + 1])
                    tempY += 1
                # Down is not none, but of the same color
                elif board[tempY + 1][tempX].color == self.color:
                    down = False
                # Down is none, and of different color
                else:
                    self.draw_circle(tempX, tempY + 1, board)
                    arr.append([tempX, tempY + 1])
                    down = False
            else:
                down = False

        tempX = self.x
        tempY = self.y
        while (up):
            if (tempY != 0):
                # Up is none
                if (board[tempY - 1][tempX] is None):
                    self.draw_circle(tempX, tempY - 1, board)
                    arr.append([tempX, tempY - 1])
                    tempY -= 1
                # Up is not none, but of the same color
                elif board[tempY - 1][tempX].color == self.color:
                    up = False
                # Up is none, and of different color
                else:
                    self.draw_circle(tempX, tempY - 1, board)
                    arr.append([tempX, tempY - 1])
                    up = False
            else:
                up = False

        return arr


class King(Pieces):
    def __init__(self, x, y, color, screen):
        super().__init__(x, y, "King", color, screen)

    def display_moves(self, board):
        arr = []
        for i in range(3):
            # Row above
            if(self.y > 0 and 0 <= self.x - 1 + i <= 7):
                if(board[self.y - 1][self.x -1 + i] is None or board[self.y -1][self.x -1 + i].color != self.color):
                    arr.append([self.x -1 + i, self.y - 1])
                    self.draw_circle(self.x -1 + i, self.y -1, board)

            # Row below
            if(self.y < 7 and 0 <= self.x - 1 + i <= 7):
                if(board[self.y+1][self.x -1 + i] is None or board[self.y + 1][self.x -1+ i].color != self.color):
                    arr.append([self.x -1 + i, self.y +1])
                    self.draw_circle(self.x -1 + i, self.y +1, board)

        # to the right
        if(self.x < 7):
            if(board[self.y][self.x + 1] is None or board[self.y][self.x + 1].color != self.color):
                arr.append([self.x + 1, self.y])
                self.draw_circle(self.x + 1, self.y, board)
        # to the left
        if(self.x > 0):
            if(board[self.y][self.x -1] is None or board[self.y][self.x -1].color != self.color):
                arr.append([self.x -1, self.y])
                self.draw_circle(self.x -1, self.y, board)

        return arr