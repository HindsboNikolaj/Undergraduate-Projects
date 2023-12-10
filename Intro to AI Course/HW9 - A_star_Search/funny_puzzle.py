# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:57:14 2021
funny_puzzle.py is about solving the 8-tile
puzzle that was discussed in class.
@author: nikol
"""
import heapq
import copy

class state_object:
    parent = None
    h = 0
    state = None
    g = 0
    def set_parent(state):
        parent = state
    def set_h_value(h_value):
        h = h_value
    def __init__(self, state, h, g, parent):
        self.state = state
        self.h = h
        self.parent = parent
        self.g = g
    def __lt__(self, other):
        return 0
  
        
        
goal =     [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

def print_succ(state):
    """
    Parameters
    ----------
    state : a 1-D list of integers of the current board
    Returns
    -------
    None. Simply prints all sucessors and their h() value

    """
    successive_states = succ(state)
    h_value = heuristic_value(state)
    for state in successive_states:
        h_value = heuristic_value(state)
        builder =''
        builder+= str(state)
        builder+= ' h='
        builder+= str(h_value)
        print(builder)

def solve(state):
    """
    Parameters
    ----------
    state :  a 1-D list of integers of the current board
    Returns
    -------
    None.

    """
    pq = []
    h= heuristic_value(state)
    #print(h)
    goal_found = False
    first_state_object = state_object(state, h, -1, None)
    if(h == 0): # Case that solve was passed the goal state
    #=====================================#+#++#+#+#!!!!!!!!!!!!!!!!!!!
        goal_found = True
        goal_state_object = first_state_object
        # Could set goal_found = True
   
    first_succ = succ(state)
    states_explored = []    # list of all states explored to avoid repitition
    states_explored.append(state)   # add first state to states explored
    
    
    for successor in first_succ: # First depth
        h = heuristic_value(successor)
        temp_state_object = state_object(successor, h, 0, first_state_object)
        heapq.heappush(pq, (h, successor, temp_state_object)) # append h+g, list, state object.
        #states_explored.append(successor)
  
    queue_length = len(pq)
    check = 0
    while(goal_found is False): # Rest of depths until goal is achieved in priority queue
        new_info = heapq.heappop(pq) # Pop from priority queue
        # Get info needed from the pop
        new_state = new_info[1]
        parent_state_object = new_info[2]
        states_explored.append(new_state)
        g = parent_state_object.g + 1
        h = parent_state_object.h
        #new_state_object = state_object(new_state, h, g, parent_state_object)
        check +=1
        #print('new state: ', new_state, h)
        # Check if game is complete at this new state
        if(h == 0):
            goal_found = True
            goal_state_object = parent_state_object
            #print(goal_state_object.parent.state)
        else:
            # Find successors otherwise
            successors = succ(new_state)
            #print(successors)
            # check if any of the successors has already been explored
            deletion_nodes = []
            for i in range(len(successors)):
                for j in range(len(states_explored)):
                    if states_explored[j] == successors[i]:
                        #print(states_explored[j], successors[i])
                        deletion_nodes.append(i)
                        
            deletion_nodes = sorted(deletion_nodes)
            deletion_nodes_no_duplicates = []
            for i in range(len(deletion_nodes)):
                if deletion_nodes[i] not in deletion_nodes_no_duplicates:
                    deletion_nodes_no_duplicates.append(deletion_nodes[i]) 
            deletion_nodes_no_duplicates = sorted(deletion_nodes_no_duplicates)
            for i in range(len(deletion_nodes_no_duplicates)): # Delete duplicate lists
                del successors[deletion_nodes_no_duplicates[i] -i]
            
            for valid_successor in successors:
                h = heuristic_value(valid_successor)
                temp_state_object = state_object(valid_successor, h, g, parent_state_object)
                heapq.heappush(pq, (h + g, valid_successor, temp_state_object))
                #print('successor ', valid_successor, ' h = ', h)
                if h == 0: # goal found
                    goal_state_object = temp_state_object
                    goal_found = True
                    break
            #print('looped')      
            current_length = len(pq)
            if current_length > queue_length:
                queue_length = current_length
    #Idk why...
    
    moves = 0
    original_state_found = False
    reverse_list = []
    # Gather data from child up
    while original_state_found is False:
        if goal_state_object.parent is None: # Passed the solve state
            builder = ''
            builder += str(goal_state_object.state)
            builder += ' h='
            builder += str(goal_state_object.h)
            reverse_list.append(builder)
            original_state_found = True
        elif goal_state_object.parent.parent is None:
            original_state_found = True
            for i in range(2):
                builder = ''
                builder += str(goal_state_object.state)
                builder += ' h='
                builder += str(goal_state_object.h)
                reverse_list.append(builder)
                goal_state_object = goal_state_object.parent
        else:
            builder = ''
            builder += str(goal_state_object.state)
            builder += ' h='
            builder+= str(goal_state_object.h)
            reverse_list.append(builder)
            goal_state_object = goal_state_object.parent
    # Reverse child up string to print, and print. 
    forward_list = reversed(reverse_list)
    for state in forward_list:
        print(state, 'moves:', moves)
        moves+=1

def succ(state):
    """
    Parameters
    ----------
    state :  a 1-D list of integers of the current board

    Returns
    -------
    A 2-D list of sucessive states.
    """
    two_state = three_by_three_state(state) # Transforms the 1D list to a 3D list
    x, y = index_of_element(two_state, 0)    # Index of 0 in state
    valid_moves = find_valid_moves(two_state, x, y) # List of coordinates to valid squares that can move
    possible_next_states = []
    # Now, move these squares and add the lists
    for i in range(len(valid_moves)):
        temp_state = copy.deepcopy(two_state)
        temp_state[x][y] = two_state[valid_moves[i][0]][valid_moves[i][1]] # move to blank
        temp_state[valid_moves[i][0]][valid_moves[i][1]] = 0 # Replace element with 0
        possible_next_states.append(temp_state)
        
    one_D_lists = []
    for i in range(len(possible_next_states)): # Make 1D list of all states
        one_D_lists.append((sum(possible_next_states[i], [])))
    
    return sorted(one_D_lists) # returns the sorted lists
    
def find_valid_moves(two_state, x, y):
    """
    Finds a list of coordinates to valid squares that can move

    Parameters
    ----------
    two_state : 2D list of the current board
    
    x : row location of the 0 element
    
    y : column location of the 0 element

    Returns
    -------
    A 2D list of coordinates of coordinates to valid squares that can move.

    """
    possible_moves = [[1, 0], [-1, 0], [0, -1], [0, 1]]
    valid_moves = []
    for move in possible_moves:
        move[0] += x 
        move[1] += y
        if move[0] < 3 and move[0] >= 0 and move[1] < 3 and move[1] >= 0: # valid move check
            valid_moves.append([move[0], move[1]])
    return valid_moves

def index_of_element(two_state, element):
    """
    Finds the location of the zero element.
    
    Parameters
    ----------
    two_state : A 2D list of the current state

    Returns
    -------
    the x, y index of element 0 in the state

    """

    for i in range(3):
        for j in range(3):
            if two_state[i][j] == element:
                x, y = i, j
    return x, y

def three_by_three_state(state):
    """
    Transforms the 1D state to a 3x3 list
    
    Parameters
    ----------
    state: a 1-D list of integers of the current board

    Returns
    -------
    A 3x3 list transformation of the 1-D list

    """
    return [state[i:i+3] for i in range(0, 9, 3)]

def heuristic_value(state):
    """
    Parameters
    ----------
    state : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
   
    two_state = three_by_three_state(state)
    h = 0
    for i in range(3):
        for j in range(3):
            if two_state[i][j] != goal[i][j]:  # If element in not in the right place
                if two_state[i][j] != 0: # do not include 0 in this score
                    x, y = index_of_element(goal, two_state[i][j])
                    h += abs(x - i) + abs(y - j) # Manhattan distance between state and goal
    return h


"""test_matrix = [1, 2, 3, 4, 5, 0, 6, 7, 8]
test_2 = [1,2,3,4,5,6,7,0,8]
solve(test_2)
solve(test_matrix)
solve([4,3,8,5,1,6,7,2,0])
#print_succ(test_matrix)
"""
#print_succ([1, 2, 3, 4, 5, 0, 6, 7, 8])
#solve([1, 2, 3, 4, 5, 0, 6, 7, 8])
#solve([4,3,8,5,1,6,7,2,0])
#solve([8, 6, 7, 2, 5, 4, 3, 0 , 1])
#print_succ([4,3,8,5,1,6,7,2,0])print_succ([4, 3, 8, 5, 1, 0, 7, 2, 6])
#print_succ([1, 2, 3, 4, 5, 0, 6, 7, 8])
#print(heuristic_value([1, 2, 3, 4, 5, 0, 6, 7, 8]))
#print_succ([6, 4, 7, 8, 5, 0, 3, 2, 1])