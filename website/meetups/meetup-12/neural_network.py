import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


# The network class contains the intializer and some methods for our neural network
# You create a network by calling Network([Nodes_Input,Nodes_2,Nodes_3,...,Nodes_Output]) 

class Network(nn.Module):
    def __init__(self, sizes):
        super(Network, self).__init__()
        self.sizes = sizes
        self.num_layers = len(sizes)
        
        self.layers = nn.ModuleList()
        for i in range(self.num_layers - 1):
            layer = nn.Linear(sizes[i], sizes[i+1])
            nn.init.xavier_normal_(layer.weight)   # Good initialization for shallow/sigmoid nets
            #nn.init.kaiming_normal_(layer.weight, mode='fan_out', nonlinearity='relu') initialization for relus
            #nn.init.kaiming_uniform_(layer.weight, mode='fan_out', nonlinearity='relu') initialization for relus and deep nets

            nn.init.zeros_(layer.bias)               # initialize the bias to 0
            self.layers.append(layer)
    
    # Forward is the method that calculates the value of the neural network. Basically we recursively apply the activations in each
    # layer
    
    def forward(self, x):
        for layer in self.layers[:-1]:
            x = F.sigmoid(layer(x))   # sigmoid layers
            # x = F.relu(layer(x)) # You will try the relu layer in the last problem
        x = self.layers[-1](x) 
        return x





def train(network, train_data, epochs, mini_batch_size, eta, test_data=None):
    # Here is where we set up the optimizer. We will try two different options, SGD with momentum and ADAM
    # I didn't go over what Nesterov acceleration was in class, but it is a slightly different way to implement momentum.
    # Using it or not is not hugely important
    # You will need to use a larger initial learning rate for SGD then ADAM
    # The weight decay is an L2 regularization, you can experiment with it but things work a lot more
    # nicely and reliably when you have it:
    
    optimizer = optim.SGD(network.parameters(),momentum=0.8,nesterov=True, lr=eta,weight_decay=1e-5)
    
    # This uncomment this (and comment the above line) if you want to use ADAM. The betas are the memory
    # parameters, you can experiment with these hyperparaeters if you like:
    #optimizer = optim.Adam(network.parameters(),betas = (0.9,0.999), lr=eta,weight_decay=1e-5)

    # Here is code for using learning rate scheduling. You might find this helpful
    #step_size = 2
    #gamma = 0.7
    #scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)

    # We are using the cross entropy loss
    
    loss_fn = nn.CrossEntropyLoss()
    
    # Here are some quantities that we are going to track in training
    # The loss history is the evaluation of the neural network on the training
    # data using the cross entropy loss, the accuracy is the out of sample accuracy
    # and the gradient ratio will be used and uncommented for problem 4 when you are going
    # to study the vanishing/exploding gradient problem
    
    loss_history = []      
    accuracy_history = []  
    train_accuracy_history = []
    # Uncomment this when it is time to explore gradients
    #grad_ratio_history = [] 
    
    # We are going to loop over the epochs
    for epoch in range(epochs):
        # This puts the network into training mode
        network.train()
        running_loss = 0.0
        batch_count = 0
        #grad_ratio_total = 0.0 Uncomment later to track the gradient ratio

        # Now we loop through the batches to train
        for data, target in train_data:
            optimizer.zero_grad() # This clears the internally stored gradients
            output = network(data) # evaluate the neural network on the minibatch, we will compare this to the target
            # Here we calculate the loss function and then use backpropagation
            # to calculate the gradient
            loss = loss_fn(output, target) 
            loss.backward()
            
            # Here is some code that we will use to look at exploding gradients
            # Get gradients for first and last layer weights
            #grad_input = network.layers[0].weight.grad
            #grad_output = network.layers[-1].weight.grad

            # Compute L2 norms
            #input_norm = grad_input.norm(2).item()
            #output_norm =grad_output.norm(2).item() 
            #grad_ratio = input_norm/(output_norm+1e-16)
            # Accumulate the grad norms for this minibatch
            #grad_ratio_total += grad_ratio

            # Update the weights
            optimizer.step()
            
            running_loss += loss.item()
            batch_count += 1
        
        
        # Track our metrics
        avg_loss = running_loss / batch_count
        loss_history.append(avg_loss)
        
        #avg_grad_ratio = total_grad_norm / batch_count
        #grad_norm_history.append(avg_grad_norm)
        
        # Compute our training set accuracy
        train_acc = evaluate(network,train_data)
        train_accuracy_history.append(train_acc)
        
        # Compute our test set accuracy
        acc = evaluate(network, test_data)
        accuracy_history.append(acc)
        
        # Update the status of our run at this epoch
        print(f"Epoch {epoch+1}: Avg loss: {avg_loss:.4f} | Test Accuracy: {acc:.4f} | Test Accuracy: {acc:.4f}% ")
    
    return loss_history, train_accuracy_history, accuracy_history


# This function evaluates the network on the test data

def evaluate(network, test_data):
    network.eval()
    correct = 0
    total = 0
    # We have the "with torch.no_grad()" line for efficiency purposes
    with torch.no_grad():
        for data, target in test_data:
            output = network(data)
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += data.size(0)
    acc = correct / total
    return acc




