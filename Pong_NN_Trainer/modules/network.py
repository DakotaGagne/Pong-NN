"""
network.py

Contains the class for the Neural Network

"""
import numpy as np

class Network:
    def __init__(self, depth, mutation_rate):
        # network has input, hidden layer, and output
        # I decide number of hidden layer neurons
        # input has 5 neurons, output has 1
        # Depth is a list with the depth of each layer. First elem and last elem should be the same every time
        self.fitness = 0  # Used to measure the best network
        self.depth = depth  # the number of neurons in the hidden layer
        self.weight_cnt = [self.depth*5, self.depth]  # the number of weights in the hidden and output layers, respectively
        self.mutation_rate = mutation_rate  # amount each weight can be mutated by
        self.weights = []
    
    def randomizeWeights(self):
        # Randomizes the weights of the network
        np.random.seed(None)
        self.weights = [
            np.random.randn(self.depth, 5) / np.sqrt(5),
            np.random.randn(self.depth) / np.sqrt(self.depth)
        ]

    def run(self, inputs):
        # Uses input values to calculate output
        hidden_layer_values = np.dot(self.weights[0], inputs)
        hidden_layer_values = self.relu(hidden_layer_values)
        global tester1
        tester1 = hidden_layer_values
        output_layer_values = np.dot(hidden_layer_values, self.weights[1])
        output_layer_values = self.sigmoid(output_layer_values)
        global tester2
        tester2 = output_layer_values
        return output_layer_values

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1.0 / (1.0 + np.exp(-x))

    def relu(self, vector):
        # ReLU activation function
        vector[vector < 0] = 0
        return vector

    def getGenome(self):
        # Returns the genome of the network
        # Used to copy the network
        # Can be removed from the program and stored
        # Also used to create children and mutate
        return self.weights[0].flatten().tolist() +\
               self.weights[1].flatten().tolist()

    def updateWeights(self, weights):
        # Updates the weights of the network, and mutates them slightly
        np.random.seed(None)
        # mutate weights by -mutation_rate to mutation_rate
        mutated_weights = []
        for j in weights:
            mutated_weights.append(j + np.random.uniform(0,
                                   2*self.mutation_rate)-self.mutation_rate)
        self.setWeights(mutated_weights)
    
    def setWeights(self, weights):
        self.weights[0] = np.asarray(weights[:self.weight_cnt[0]]).reshape(self.depth, 5)
        self.weights[1] = np.asarray(weights[self.weight_cnt[0]:]).reshape(self.depth)


if __name__ == '__main__':
    print("This is a module. Not meant to be run standalone.")