# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__()
        # certain definitions
        # First convolution layer
        self.conv1 = nn.Conv2d(in_channels = 3, out_channels = 6, 
                    kernel_size = 5, stride = 1, padding = 0, bias = True)
        # First convolution layer pool
        self.pool1 = nn.MaxPool2d(kernel_size = 2, padding = 0, stride = 2)
        
        # Second convolution layer
        self.conv2 = nn.Conv2d(in_channels = 6, out_channels = 16, kernel_size = 5,
                    stride = 1, padding = 0, bias = True)

        # Second convolution layer pool
        self.pool2 = nn.MaxPool2d(kernel_size = 2, padding = 0, stride = 2)
        
        # Fully connected layer
        self.fc1 = nn.Linear(16*5*5, 256, bias = True)
        self.fc2 = nn.Linear(256, 128, bias = True)
        self.fc3 = nn.Linear(128, 100, bias = True)
        
        #Flatten layer (3D --> 1D tensor)
        #self.fc1 = torch.nn.        
        
    def forward(self, x):
        shape_dict = {}
        # certain operations
        
        
        # reulu activation layer after first convolution layer
        x = nn.functional.relu(self.conv1(x))
        # first convolution layer max_pool
        x = self.pool1(x)
        # First layer done - now add to dictionary
        shape_dict[1] = list(x.shape)
        
        # relu activation layer after second convolution layer
        x = nn.functional.relu(self.conv2(x))
        # second max_pool
        x = self.pool2(x)
        # Second layer done - now add to dictionary
        shape_dict[2] = list(x.shape)
        
        x = x.view(-1, 16*5*5)  # 1-D tensor of size 400 (Output total)
        # Third layer done - now add to dictionary
        shape_dict[3] = list(x.shape)
        
        # FC-1, perform ReLU non-linearity
        x = nn.functional.relu(self.fc1(x))
        # Fourth layer - add to dictionary
        shape_dict[4] = list(x.shape)
        
        # FC-2, perform ReLU non-linearity
        x = nn.functional.relu(self.fc2(x))
        # Fifth layer - add to dictionary
        shape_dict[5] = list(x.shape)
        
        # FC-3
        x = self.fc3(x)
        # Last layer - add to dictionary
        shape_dict[6] = list(x.shape)
        
        return x, shape_dict


def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    total_params = 0
    model = LeNet()
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad: continue
        param = parameter.numel()
        total_params += param
    return total_params/1e6


def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        ###################################
        # fill in the standard training loop of forward pass,
        # backward pass, loss computation and optimizer step
        ###################################

        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        # Uncomment the below line after you fill block 1 and 2
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc

 
    