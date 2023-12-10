import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import math
# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_dataset(filename):
    """
    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """
    dataset = np.loadtxt(filename, delimiter = ',', skiprows = 1, usecols = range(1, 17))
    return dataset


def print_stats(dataset, col):
    """
    print_stats prints the 
    1. number of data points
    2. sample mean
    3. sample standard deviation
    of the column specified in the dataset.

    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.

    RETURNS:
        None
    """
    column_array = dataset[:,col]
    print(len(column_array))
    print("{:.2f}".format(my_mean(column_array)))
    print("{:.2f}".format(my_std(column_array)))
    
"""
Helper method - put in comments
"""
def my_mean(column_array):
    total = 0
    for num in column_array:
        total += num
    return total/len(column_array)


"""
Helper method - put in comments
"""
def my_std(column_array):
    total = 0
    mean = my_mean(column_array)
    for num in column_array:
        total += (num-mean)**2
    return math.sqrt(total/(len(column_array)-1))


def regression(dataset, cols, betas):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    mse = 0
    col_array = []
    for col_num in cols: 
        col_array.append(dataset[:,col_num]) # get all column data
    body_fat_column = dataset[:,0] # bodyfat column being compared
    temp = 0
    for i in range(len(body_fat_column)):
        temp = betas[0]     #B0
        for j in range(len(col_array)): #B1x1 + B2x2 + ... + Bnxn for ith row
            temp += betas[j+1]*col_array[j][i]
        temp -= body_fat_column[i] # ith row of bodyfat (y_i)
        temp = math.pow(temp, 2)
        mse += temp
            
    return mse / len(body_fat_column)   # 1/n * sum of regressions


def gradient_descent(dataset, cols, betas):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads =[]
    grads.append(general_gradient(dataset, cols, betas, -1))
    for i in range(len(betas)-1):
        grads.append(general_gradient(dataset, cols, betas, i))
    return np.array(grads)

def general_gradient(dataset, cols, betas, x_i):
    total = 0
    col_array = []
    for col_num in cols: 
        col_array.append(dataset[:,col_num]) # get all column data
    body_fat_column = dataset[:,0] # bodyfat column being compared
    temp = 0
    for i in range(len(body_fat_column)):
        temp = betas[0]     #B0
        for j in range(len(col_array)): #B1x1 + B2x2 + ... + Bnxn for ith row
            temp += betas[j+1]*col_array[j][i]
        temp -= body_fat_column[i] # ith row of bodyfat (y_i)
        if x_i != -1:   #for all partials
            temp *= col_array[x_i][i]
        total += temp
    return 2*total/(len(body_fat_column))

def iterate_gradient(dataset, cols, betas, T, eta):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    gradients = gradient_descent(dataset, cols, betas)
    for i in range(T):
        for j in range(len(betas)):
            betas[j] = betas[j] - eta*gradients[j]
        # first get the "new" gradients
        gradients = gradient_descent(dataset, cols, betas)
        # then, get the "new" MSE
        current_mse = regression(dataset, cols, betas)
        two_dec_betas = []
        for k in range(len(betas)):
            two_dec_betas.append("{:.2f}".format(betas[k]))
        # print all the values for current time.
        print(i+1, "{:.2f}".format(current_mse), *two_dec_betas, sep = " ")
        # now, set up the next beta values.
        
        
def compute_betas(dataset, cols):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    betas = None
    body_fat_column = dataset[:,0]
    col_array = []
    for col_num in cols: 
        col_array.append(dataset[:,col_num]) # get all column data
    length = len(col_array[0])
    x_array = np.ones((length, len(col_array) + 1))
    col_array = np.array(col_array)
    #Now, creating the real x-array
    for j in range(len(col_array)): # for each number of columns
        x_array[:,j+1] = col_array[j] # creating array "x"
            
    
    temp = np.transpose(x_array)
    to_be_inversed = np.dot(temp, x_array)
    inversed = np.linalg.inv(to_be_inversed)
    temp = np.dot(temp, body_fat_column)
    betas = np.dot(inversed, temp)
    
    mse = regression(dataset, cols, betas)
    return (mse, *betas)


def predict(dataset, cols, features):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    mse, *betas = compute_betas(dataset, cols)
    
    result = betas[0]
    for i in range(len(betas)-1):
        result += features[i]*betas[i+1]
    return result


def synthetic_datasets(betas, alphas, X, sigma):
    """
    Input:
        betas  - parameters of the linear model
        alphas - parameters of the quadratic model
        X      - the input array (shape is guaranteed to be (n,1))
        sigma  - standard deviation of noise

    RETURNS:
        Two datasets of shape (n,2) - linear one first, followed by quadratic.
    """
    
    n = X.shape[0]
    X = X[:,0]
    
    linear_array = np.zeros((n, 2))
    first_column = linear_array[:,0]
    first_column += float(betas[0])
    X_temp = X.copy()*betas[1]
    first_column += X_temp
    mu, sigma = 0, sigma
    noise_array = np.random.normal(loc = 0, scale = sigma, size = n)
    noise_array.reshape((1, n))
    first_column += noise_array
    linear_array[:,1] = X
    quadratic_array = np.zeros((n, 2))
    first_column = quadratic_array[:,0]
    first_column += float(alphas[0])
    X_temp = (X.copy()**2)*alphas[1]
    first_column += X_temp
    noise_array = np.random.normal(loc = 0, scale = sigma, size = n)
    noise_array.reshape((1, n))
    first_column += noise_array
    quadratic_array[:,1] = X
    return linear_array, quadratic_array


def plot_mse():
    
    #print(input_array)
    from sys import argv
    if len(argv) == 2 and argv[1] == 'csl':
        import matplotlib
        matplotlib.use('Agg')
    input_array = np.zeros((1000, 1))
    temp = np.random.uniform(-100, 100, size = 1000) # creating 1000 numbers [-100, 100] range (random)
    input_array[:,0] += temp
    sigmas = np.ones((1, 10))
    for i in range(len(sigmas[0])):
        sigmas[0][i] *= 10**(i-4) # creating sigma array
    alphas = np.random.uniform(0.2, 1, size = 2) # creating alphas
    betas = np.random.uniform(0.2, 1, size = 2) # creating betas
    
    lin_synthetic_data = []
    quad_synthetic_data = []
    for i in range(len(sigmas[0])):
        temp = synthetic_datasets(betas, alphas, input_array, sigmas[0][i])
        lin_synthetic_data.append(temp[0])
        quad_synthetic_data.append(temp[1])
    lin_synthetic_data = np.array(lin_synthetic_data)
    quad_synthetic_data = np.array(quad_synthetic_data)
    lin_data = []
    quad_data = []
    for i in range(10):
        lin_data.append(compute_betas(lin_synthetic_data[i], cols = [1]))
        quad_data.append(compute_betas(quad_synthetic_data[i], cols = [1]))
    lin_data = np.array(lin_data)
    quad_data = np.array(quad_data)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel('Sigma')
    ax.set_ylabel('MSE')
    plt.plot(sigmas[0], lin_data[:,0], label = "linear", marker = 'o')
    plt.plot( sigmas[0], quad_data[:,0], label = "quadratic", marker = 'o')
    plt.legend()
    fig.savefig("mse.pdf", bbox_inches = 'tight')
    # TODO: Generate datasets and plot an MSE-sigma graph


if __name__ == '__main__':
    ### DO NOT CHANGE THIS SECTION ###
    plot_mse()


