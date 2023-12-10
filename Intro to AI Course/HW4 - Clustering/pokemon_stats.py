# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 21:03:16 2021

@author: nikol
"""
import csv
import numpy as np
import scipy.cluster
from random import randrange
import math
import matplotlib.pyplot as plt
"""Load a CSV file and store the first 20 data points
    ----------------------------------------
    given - filepath
    ----------------------------------------
    returns - list of dictionaries"""

def load_data(filepath):
    dictionaries = []
    input_file = csv.DictReader(open(filepath))
    i = 0
    
    #Creating the list of dictionaries
    int_values = ['#', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    for row in input_file:
        if i < 20:
            dictionaries.append(row)
        else:
            break
        i += 1
   
    #Getting rid of the generation and legendary stats
    for i in range(len(dictionaries)):
        dictionaries[i].pop('Generation')
        dictionaries[i].pop('Legendary')
    #changing from string to int values
    for i in range(20):
        current_row = dictionaries[i]
        for j in range(len(int_values)):
            current_row[int_values[j]] = int(current_row[int_values[j]])
    #Return the list of dictionaries
    
    return dictionaries

"""Calculates the x - Offensive Strength
    And the y - Defensive Strength of the pokemon.
    Returns the values in a tuple (x, y)
    -------------------------------------------
    given - stats - a dictionary of stats of a specific pokemon
    -------------------------------------------
    returns - a tuple (x, y) of of offensive and defensive stats (calcaulted)
    
    """
    
def calculate_x_y(stats):
    #Attack (x) calculated as:
    #       Attack + Sp. Attack + Speed
    x = 0
    attributes = ["Attack", "Sp. Atk", "Speed"]
    for i in range(len(attributes)):
        x += int(stats[attributes[i]])
    #Defense (y) calcualted as:
    #       Defense + Sp. Def + HP
    y = 0
    attributes = ["Defense", "Sp. Def", "HP"]
    for i in range(len(attributes)):
        y += int(stats[attributes[i]])
    
    return (x, y)

"""Performs single linkage hierachal agglomerative clustering on the Pokemon
   with the (x, y) feature representation, 
   and returns a data structure representing the cluster.
   ----------------------------------------
   given - dataset - 
   ----------------------------------------
   returns - 
"""

def hac(dataset):
    real_data = remove_invalid(dataset)
    m = len(real_data)
    distance_matrix = create_diagonal(real_data)
    dict_all_indices = {}
    current_index = m
    linkage_list = []
    num_linked = 0
    for i in range(m):
        dict_all_indices[i] = i #create a dict of indices (to be used in clusters later)
    for i in range(m-1): #create m-1 x 4 rows of clusters
        new_distance_found = False
        num_linked = 0
        while(new_distance_found is False):
            c1, c2, min_distance, distance_matrix = find_next_smallest(distance_matrix, dict_all_indices)
            if c1 != c2: # if c1 is not in cluster c2
                new_distance_found = True
                for j in range(m):
                    if dict_all_indices[j] == c1 or dict_all_indices[j] == c2:
                        dict_all_indices[j] = current_index + i
                        num_linked += 1
                linkage_list.append([c1, c2, min_distance, num_linked])
                dict_all_indices[c1] = current_index + i   #put c1 in cluster m+i
                dict_all_indices[c2] = current_index + i   #put c2 in cluster m+i
                
    return np.array(linkage_list)

def remove_invalid(dataset):
    length = len(dataset)
    final_set = []
    for i in range(length):
        add_to_set = True
        x = dataset[i][0]
        y = dataset[i][1]
        if math.isnan(x) is True or math.isnan(y) is True: #check for nan values
            add_to_set = False
        if math.isinf(x) is True or math.isinf(y) is True:
            add_to_set = False
        if add_to_set is True:
            final_set.append((x, y))
    return final_set    
        
def create_diagonal(list_tuples):
    m = len(list_tuples)
    distance_matrix = np.zeros((m,m))
    for i in range(m):
        for j in range(m):
            distance_matrix[i][j] = euclidean_distance(list_tuples[i], list_tuples[j])
            if i == j:
                distance_matrix[i][j] = -1
    return distance_matrix
    
#returns c1, c2, distance, and new distance matrix.
def find_next_smallest(distance_matrix, dictionary_list):
    #goes through distance matrix, finding the smallest distance != -1
    m = len(distance_matrix)
    current_min = -1
    c1 = 0
    c2 = 0
    i_value = 0
    j_value = 0
    for i in range(m):
        for j in range(m):
            if current_min == -1 and distance_matrix[i][j] != -1: #good
                current_min = distance_matrix[i][j]
                c1 = dictionary_list[i]
                c2 = dictionary_list[j]
                i_value = i
                j_value = j
                if c1 > c2: #ordering c1, c2
                    temp_c3 = c1
                    c1 = c2
                    c2 = temp_c3
                    temp_i = i_value
                    i_value = j_value
                    j_value= temp_i
            elif current_min > distance_matrix[i][j] and distance_matrix[i][j] != -1: #new min found
                current_min = distance_matrix[i][j]
                c1 = dictionary_list[i]
                c2 = dictionary_list[j]
                i_value = i
                j_value = j
                if c1 > c2: #ordering c1, c2
                    temp_c3 = c1
                    c1 = c2
                    c2 = temp_c3
                    temp_i = i_value
                    i_value = j
                    j_value= temp_i
            if current_min == distance_matrix[i][j] and distance_matrix[i][j] != -1: #tiebreaker
                c4 = dictionary_list[i]
                c5 = dictionary_list[j]
                temp_i = i
                temp_j = j
                if c4 > c5: #ordering c4, c5
                    temp_c6 = c4
                    c4 = c5
                    c5 = temp_c6
                    temp_temp_i = temp_i
                    temp_i = temp_j
                    temp_j = temp_temp_i
                if c4 < c1: #c1 was greater, so replace.
                    c1 = c4
                    c2 = c5
                    i_value = temp_i
                    j_value = temp_j
                elif c4 == c1: #double tie-breaker
                    if c5 < c2: #c2 was greater, so replace.
                        c1 = c4
                        c2 = c5
                        i_value = temp_i
                        j_value = temp_j
    distance_matrix[i_value][j_value] = -1
    distance_matrix[j_value][i_value] = -1
    #Now the minimum is found.
    return c1, c2, current_min, distance_matrix
            



def euclidean_distance(tuple1, tuple2):
    delta_x = tuple2[0]-tuple1[0]
    delta_y = tuple2[1]-tuple1[1]
    return math.sqrt((delta_x**2)+(delta_y**2))

# Takes the number of samples we want to randomly generae, and returns
#these samples in a single structure.

def random_x_y(m):
    pokemon_list = []
    for i in range(m):
        x = randrange(359) + 1
        y = randrange(359) + 1
        pokemon_list.append((x, y))
    return pokemon_list

#Performs single linkage hierarchial agglomerative clustering on the Pokemon with
#(x, y) feature represenation, and imshow the clustering process
def imshow_hac(dataset):   
    #Now, plot the lines connecting them.
    real_data = remove_invalid(dataset)
    m = len(real_data)
    x_data = []
    y_data = []
    plt.ion()
    for i in range(m):
        x_data.append(real_data[i][0])
        y_data.append(real_data[i][1])
    distance_matrix = create_diagonal(real_data)
    figure = plt.figure()
    plt.scatter(x_data, y_data)
    plt.pause(0.1) # plotted all data points
    dict_all_indices = {}
    current_index = m
    linkage_list = []
    num_linked = 0
    for i in range(m):
        dict_all_indices[i] = i #create a dict of indices (to be used in clusters later)
    for i in range(m-1): #create m-1 x 4 rows of clusters
        new_distance_found = False
        num_linked = 0
        while(new_distance_found is False):
            c1, c2, min_distance, distance_matrix, i_value, j_value = find_next_smallest_im(distance_matrix, dict_all_indices)
            if c1 != c2: # if c1 is not in cluster c2
                new_distance_found = True
                for j in range(m):
                    if dict_all_indices[j] == c1 or dict_all_indices[j] == c2:
                        dict_all_indices[j] = current_index + i
                        num_linked += 1
                linkage_list.append([c1, c2, min_distance, num_linked])
                dict_all_indices[c1] = current_index + i   #put c1 in cluster m+i
                dict_all_indices[c2] = current_index + i   #put c2 in cluster m+i
        x_data_2 = [real_data[i_value][0], real_data[j_value][0]]
        y_data_2 = [real_data[i_value][1], dataset[j_value][1]]
        plt.plot(x_data_2, y_data_2)
        plt.pause(0.1)
    #hac_data = hac(dataset)
    #plt.scatter(hac_data)
    #plt.pause(0.1)
    #plt.plot(hac_data)
    plt.show()

def find_next_smallest_im(distance_matrix, dictionary_list):
    #goes through distance matrix, finding the smallest distance != -1
    m = len(distance_matrix)
    current_min = -1
    c1 = 0
    c2 = 0
    i_value = 0
    j_value = 0
    for i in range(m):
        for j in range(m):
            if current_min == -1 and distance_matrix[i][j] != -1: #good
                current_min = distance_matrix[i][j]
                c1 = dictionary_list[i]
                c2 = dictionary_list[j]
                i_value = i
                j_value = j
                if c1 > c2: #ordering c1, c2
                    temp_c3 = c1
                    c1 = c2
                    c2 = temp_c3
                    temp_i = i_value
                    i_value = j_value
                    j_value= temp_i
            elif current_min > distance_matrix[i][j] and distance_matrix[i][j] != -1: #new min found
                current_min = distance_matrix[i][j]
                c1 = dictionary_list[i]
                c2 = dictionary_list[j]
                i_value = i
                j_value = j
                if c1 > c2: #ordering c1, c2
                    temp_c3 = c1
                    c1 = c2
                    c2 = temp_c3
                    temp_i = i_value
                    i_value = j
                    j_value= temp_i
            if current_min == distance_matrix[i][j] and distance_matrix[i][j] != -1: #tiebreaker
                c4 = dictionary_list[i]
                c5 = dictionary_list[j]
                temp_i = i
                temp_j = j
                if c4 > c5: #ordering c4, c5
                    temp_c6 = c4
                    c4 = c5
                    c5 = temp_c6
                    temp_temp_i = temp_i
                    temp_i = temp_j
                    temp_j = temp_temp_i
                if c4 < c1: #c1 was greater, so replace.
                    c1 = c4
                    c2 = c5
                    i_value = temp_i
                    j_value = temp_j
                elif c4 == c1: #double tie-breaker
                    if c5 < c2: #c2 was greater, so replace.
                        c1 = c4
                        c2 = c5
                        i_value = temp_i
                        j_value = temp_j
    distance_matrix[i_value][j_value] = -1
    distance_matrix[j_value][i_value] = -1
    #Now the minimum is found.
    return c1, c2, current_min, distance_matrix, i_value, j_value



