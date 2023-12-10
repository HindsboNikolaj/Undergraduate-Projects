import random
import copy
import time

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = self.is_drop_phase(state) # checks if the current state is in the drop phase
        all_next_states = self.succ(state)
        #print(len(all_next_states))
        max_heuristic = -2
        if drop_phase is True:
            for possible_state in all_next_states:
                temp_heuristic = self.heuristic_game_value(possible_state)
                if max_heuristic < temp_heuristic:
                    max_heuristic = temp_heuristic
                    max_state = possible_state
            new_max_state = max_state
        else:
            new_max_state= self.max_value(state, 0)[0]
            
            
        
        #print(max_state)
        # implement function to find move of the new max state
        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = self.return_move_based_on_state(state, new_max_state)
        
        """(row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))"""
        
        return move

    def max_value(self, state, depth):
        current_heuristic = self.heuristic_game_value(state)
        if depth == 2 or current_heuristic == 1: # max depth or terminal state
            return [state, self.heuristic_game_value(state), depth]
        else: 
            all_next_states = self.succ(state) # get all new states
        max_tree = -2
        for next_state in all_next_states: # finding best child
            val_of_tree = self.max_value(next_state, depth+1)
            if val_of_tree[1] == 1 and val_of_tree[2] == depth+1: # endstate found
                return [val_of_tree[0], 1-depth/10, depth+1]
            if val_of_tree[1] > max_tree: # Largest new tree
                max_next_state = next_state
                max_tree = val_of_tree[1]
        # Now that all next trees have been evaluated, return current value + value of max tree
        return [max_next_state, max_tree+current_heuristic, depth]
                
            
    
    def return_move_based_on_state(self, current_state, next_state):
        """
        

        Parameters
        ----------
        current_state : TYPE
            DESCRIPTION.
        next_state : TYPE
            DESCRIPTION.

        Returns
        -------
        A legal move for the AI to take.

        """
        change_list = []
        for i in range(5):
            for j in range(5):
                if current_state[i][j] != next_state[i][j]: # one of the two changes
                    change_list.append((i, j))
        if len(change_list) == 1:
            return [(change_list[0][0], change_list[0][1])]
        else: # need to find which piece is source, which one is new move.
            if current_state[change_list[0][0]][change_list[0][1]] == self.my_piece: # first coordinates is current state
                return [(change_list[1][0], change_list[1][1]), (change_list[0][0], change_list[0][1])]
            else: # second coordinate list is current state
                return[(change_list[0][0], change_list[0][1]), (change_list[1][0], change_list[1][1])]

    
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1                    
        # TODO: check / diagonal wins
        for row in range(3, 5): # CHECKING THAT THIS WAS EDITED
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row-1][col+1] == state[row-2][col+2] == state[row-3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1   
        # TODO: check 3x3 square corners wins
        vector_checks = [[-1, -1], [1, 1], [-1, 1], [1, -1]]
        for row in range(3):
            for col in range(3): #Check all centers
                game_over = True
                for i in range(4):  # number of vector checks
                    if i == 0: # Set first check
                        check = state[row+1+vector_checks[i][0]][col+1+vector_checks[i][1]]
                        if check == ' ': # If there's nothing to check
                            game_over = False
                    else:
                        if check != state[row+1+vector_checks[i][0]][col+1+vector_checks[i][1]]:
                            game_over = False # Game is not over if just one of these is not equal to the check
                if game_over is True: # 3x3 satisfied
                    return 1 if check == self.my_piece else -1   
                    
        return 0 # no winner yet

    def succ(self, state):
        """
        
        Parameters
        ----------
        state : (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.
        Returns
        -------
        A list of the legal successors.
        """
        drop_phase = self.is_drop_phase(state) # checks if current state is in the drop phase
        if drop_phase is True: # If currently in the drop phase
            list_of_states = self.find_all_drop_phase_states(state) # Find all states possible from drop phase
                        
        else: # State not in drop phase
            list_of_states = self.find_all_post_drop_phase_states(state) # Find all post-drop states
                   
        return list_of_states
            
    def find_all_drop_phase_states(self, state):
        """
        Assuming that it's the drop phase of the game, returns all possible moves.

        Parameters
        ----------
        state :  state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns
        -------
        list_of_states : A list of all the possible new states.

        """
        list_of_states = []
        list_of_moves = []
        for i in range(5): # Loop through rows
                for j in range(5): # Loop through columns (All spaces)
                    if state[i][j] == ' ': # legal move possibility
                        list_of_moves.append([i, j])
        for new_move in list_of_moves: # looping through valid moves
                temp_state = copy.deepcopy(state)
                temp_state[new_move[0]][new_move[1]] = self.my_piece # add move to new state  
                list_of_states.append(temp_state) # append state to list of states
                
        return list_of_states # list of all legal sucessive states
    
    def find_all_post_drop_phase_states(self, state):
        """
        Assuming that it's the post-drop phase of the game, returns all possible moves
        Parameters
        ----------
        state :  state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns
        -------
        list_of_states : List of all possible new states 

        """
        move_vectors = [[1, 0], [-1, 0], [0, 1], [0, -1],   #Left, right, up, down
                        [-1, -1], [1, 1], [-1, 1], [1, -1]] # diagonals
        list_of_states = []
        temp_piece_state = []
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece: # if current spot is ai's piece
                    temp_piece_state = (self.piece_legal_moves((i,j), state, move_vectors)) # Add list of states for current piece
                    for each_state in temp_piece_state:
                        list_of_states.append(each_state)
        return list_of_states
            
        
    # TODO - 
    def piece_legal_moves(self, piece_location, state, move_vectors):
        """
        Returns all of the legal moves of a single piece in the post-drop phase
        Assumes current piece location given is a valid piece, that self owns.
        
        Parameters
        -----------
        piece_location: tuple of piece location (x, y) in matrix
        
        state:  state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.
        
        move_vectors: legal move vector.
        
        Returns
        ---------
        piece_legal_states - all legal states for that piece
        """
        x = piece_location[0]
        y = piece_location[1]
        piece_legal_states = []
        for i in range(8): # check all possible moves (The eight surrounding)
            temp_x = x + move_vectors[i][0] # x being checked
            temp_y = y + move_vectors[i][1] # y being checked
            if temp_x > -1 and temp_x < 5 and temp_y > -1 and temp_y < 5: # check if new state is out of bounds
                if state[temp_x][temp_y] == ' ': # check valid move (nothing is there already)
                    temp_state = copy.deepcopy(state)   # deep copy of state to copy
                    temp_state[temp_x][temp_y] = self.my_piece # move to new square
                    temp_state[x][y] = ' ' # "move from" old square
                    piece_legal_states.append(temp_state)
        return piece_legal_states
    
    def heuristic_game_value(self, state):
        """
        Evaluates non-terminal states. 
        Parameters
        ----------
        state : (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.
        Returns
        -------
        A floating-point value between 1 and -1, where a score
        towards 1 represents a favorable position for the AI, and a score
        towards -1 represents a favorable position for the Computer.

        """
        # The game_value method should be called here to determine if 
        # the current state of the game is terminal.
        check = self.game_value(state)
        if check == -1 or check ==1:
            return check
        
        diagonal_score = self.calculate_diagonal_score(state)
        four_score = self.calculate_four_score(state)
        square_score = self.calculate_square_score(state)
        total_score = diagonal_score + four_score + square_score
        return diagonal_score/10000
    
    def calculate_diagonal_score(self, state):
        """
        
        Parameters
        ----------
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        An arbitrary value, based on how favorable the current state is 
        related to its diagonal winning potential

        """
        all_diags = self.get_all_diagonal_lists(state)
        total_diagonal_score = 0
        for diag_list in all_diags: # evaluate each diagonal
           total_diagonal_score += self.individual_diagonal_score(diag_list)
        return total_diagonal_score
    
    def get_all_diagonal_lists(self, state):
        """
        gets all the diagonal lists in the state

        Parameters
        ----------
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        A 2D list of diagonal lists.

        """        
        list_of_diagonals = []
        #left down
        list_of_diagonals.append([state[i][i] for i in range(len(state))])
        list_of_diagonals.append([state[i][i-1] for i in range(1, len(state))])
        list_of_diagonals.append([state[i][i+1] for i in range(len(state)-1)])
        # up right
        list_of_diagonals.append([state[i][len(state)-1-i] for i in range(len(state))])
        list_of_diagonals.append([state[i-1][len(state)-i-1] for i in range(1, len(state))])
        list_of_diagonals.append([state[i+1][len(state)-i-1] for i in range(len(state)-1)])
        return list_of_diagonals
        
        
    def individual_diagonal_score(self, diagonal_list):
        """
        Calculates the score of an individual list of diagonals.

        Parameters
        ----------
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        0 if the opponent is in the diagonal list
        0 if no self pieces in diagonal
        amount of self pieces^2*len(diagoan_list) - an arbitrary positive score otherwise

        """
        if self.opp in diagonal_list:
            return 0
        else:
            return diagonal_list.count(self.my_piece)**2 * len(diagonal_list)

    def calculate_four_score(self, state):
        """
        
        Parameters
        ----------
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        An arbitrary value, based on how favorable the current state is 
        related to its for in a row winning potential

        """
        return 0
    
    def calculate_square_score(self, state):
        """
        
        Parameters
        ----------
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        An arbitrary value, based on how favorable the current state is 
        related to its 3x3 winning potential

        """
        return 0
    
    def is_drop_phase(self, state):
        """
        Checks to see if the current board is in the drop phase
        
        Parameters
        ----------
        state : (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns
        -------
        True - If state is currently in the drop phase
        False - state is not in the drop phase
        """     
        
        # Check if there are 8 dropped pieces, by checking if 17 ' ' is present.
        return (sum(x.count(' ') for x in state)) != 17 
    
############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
