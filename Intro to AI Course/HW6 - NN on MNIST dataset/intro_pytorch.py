import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    #our custom transformer 
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    # If training = True, load the training set
    if training is True:
    	data_set = datasets.MNIST('./data', train=True, download=True,
                       transform=custom_transform)
    # Otherwise, load the testing set
    else:
    	data_set = datasets.MNIST('./data', train=False,
                       transform=custom_transform)

        
    #retrieving data
    loader = torch.utils.data.DataLoader(dataset = data_set, batch_size = 50)
    
    return loader


def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    #model will - flatten latey 2D pixel array --> 1D
    # with dense layers
    #	128 Nodes and relU activation
    #	64 Nodes and relU activation
    # 	Dense layer with 10 nodes
    model = nn.Sequential(
    	nn.Flatten(),
    	nn.Linear(784, 128),
    	nn.ReLU(),
    	nn.Linear(128,64),
    	nn.ReLU(),
    	nn.Linear(64, 10)
    )
    return model


def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for epoch in range(T):
    	running_loss = 0.0
    	total = 0
    	correct = 0
    	for i, data in enumerate(train_loader, 0):
    		#get inputs, data : list [inputs, labels]
    		images, labels = data
    		temp_num = len(images)
    		#zero parameter gradients
    		opt.zero_grad()		
    		# forward + backward optimizer
    		outputs = model(images)
    		loss = criterion(outputs, labels)
    		loss.backward()
    		opt.step()
    		tem, predicted = torch.max(outputs.data, 1)
    		total += labels.size(0)
    		correct += (predicted == labels).sum().item()
    		#Print stats
    		running_loss += loss.item()
    	#for each epoch, print stats
    	percent_correct = correct/total*100.0
    	loss_display = running_loss*temp_num/total
    	#ex output: ​Train Epoch: 0   Accuracy: 47771/60000(79.62%) Loss: 0.740
    	print("Train Epoch: {:d}  Accuracy: {:d}/{:d}({:.2f}%)  Loss: {:.3f}".format(epoch, correct, total, percent_correct, loss_display))
    	running_loss = 0.0
    


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    model.eval()
    running_loss = 0.0
    total = 0
    correct = 0
    with torch.no_grad():
    	for data, labels in test_loader:
    		#get inputs, data : list [inputs, labels]
    		temp_num = len(data)
    		#zero parameter gradients		
    		# forward + backward optimizer
    		outputs = model(data)
    		loss = criterion(outputs, labels)
    		tem, predicted = torch.max(outputs.data, 1)
    		total += labels.size(0)
    		correct += (predicted == labels).sum().item()
    		#Print stats
    		running_loss += loss.item()
    percent_correct = correct/total*100.0
    loss_display = running_loss/total
    if show_loss is True:
    	print("Average loss: {:.4f}".format(loss_display))
  
    print("Accuracy: {:.2f}%".format(percent_correct))

def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    class_correct = list(0 for i in range(len(class_names)))
    class_total = list(0 for i in range(len(class_names)))
    model.eval()
    with torch.no_grad():
    	logits = model(test_images[index])
    	prob = F.softmax(logits, dim = 1)
    	top_three, indices = torch.topk(prob.flatten(), 3)
    for i in range(3):
    	print(f"{class_names[indices[i]]}: {(top_three[i]*100):.2f}%")
    	
    		
    		


if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
    
    
