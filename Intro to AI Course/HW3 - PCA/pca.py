from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    x = np.load(filename)
    mean = np.mean(x, axis = 0)
    return x - mean
    
def get_covariance(dataset):
    return 1/(len(dataset)-1)*np.dot(np.transpose(dataset), dataset)

def get_eig(S, m):
    num = len(S)
    eigh_values = eigh(S, subset_by_index = [num-m, num-1])
    decending_lambda = eigh_values[0]
    assending_lambda = decending_lambda[::-1]
    eig_diag = np.diag(assending_lambda)
    eig_vals = eigh_values[1]
    eig_vals = np.flip(eig_vals, axis = 1)
    return eig_diag, eig_vals
def get_eig_perc(S, perc):
    eigh_matrices = eigh(S)
    all_eigh_values = eigh_matrices[0]
    total_eigh = sum(all_eigh_values)
    i = 0
    minFound = False
    while minFound == False:
        if (all_eigh_values[i]/total_eigh) > perc:
            minFound = True
            i -= 1
        i += 1
    return get_eig(S, len(S)-i)
    
def project_image(img, U):
    alpha_values = np.dot(img, U) # List of all alpha values
    transpose = np.transpose(U)
    for i in range(len(alpha_values)):
        transpose[i] = alpha_values[i]*transpose[i] #multiplying alpha values by the eigenvectors
    x_projected = np.zeros(len(img)) # 2D matrix with size d
    for i in range(len(transpose)): # looping over m
        for j in range(len(img)):   # looping over img length (1024)
            x_projected[j] += transpose[i][j] # adding alphaij uj
    return x_projected # return projected values 

def display_image(orig, proj):
    fig = plt.figure(figsize = (10, 32))
    ax = []
    orig = np.reshape(orig, (32, 32))
    orig = np.rot90(orig, 3)
    orig = np.flip(orig, axis = 1)
    proj = np.reshape(proj, (32, 32))
    proj = np.rot90(proj, 3)
    proj = np.flip(proj, axis = 1)
    ax.append(fig.add_subplot(1, 2, 1))
    pos = plt.imshow(orig, interpolation='nearest', aspect = 'equal')
    fig.colorbar(pos, ax=ax[0], fraction = .046, pad = 0.04)    
    ax.append(fig.add_subplot(1, 2, 2))
    pos = plt.imshow(proj, interpolation='nearest', aspect = 'equal')
    fig.colorbar(pos, ax=ax[1], fraction =.046, pad = .04)
    ax[0].set_title("Original") #Original title
    ax[1].set_title("Projection") #Projeciton title
    plt.show()


