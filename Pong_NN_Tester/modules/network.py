# ----- PONG NEURAL NETWORK ----- #
"""
Plan
1. Figure out how to write network
2. Write network

- The network should have adjustable layers and depths, this would allow for
    adjustment so I can find the best network
- Need the relu function and the sigmoid function as well as the sigmoid derivative

"""
import numpy as np
import math
import random

class Network:
    def __init__(self, depth):
        self.depth = depth  # the number of neurons in the hidden layer
        self.weight_cnt = [self.depth*5, self.depth]  # the number of weights in the hidden and output layers, respectively
        self.weights = [[],[]]

    def run(self, inputs):
        hidden_layer_values = np.dot(self.weights[0], inputs)
        hidden_layer_values = self.relu(hidden_layer_values)
        output_layer_values = np.dot(hidden_layer_values, self.weights[1])
        output_layer_values = self.sigmoid(output_layer_values)
        return output_layer_values

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def relu(self, vector):
        vector[vector < 0] = 0
        return vector

    def getGenome(self):
        return self.weights[0].flatten().tolist() +\
               self.weights[1].flatten().tolist()
    
    def randomizeWeights(self):
        np.random.seed(None)
        self.weights = [
            np.random.randn(self.depth, 5) / np.sqrt(5),
            np.random.randn(self.depth) / np.sqrt(self.depth)
        ]

    def setWeights(self, weights):
        self.weights[0] = np.asarray(weights[:self.weight_cnt[0]]).reshape(self.depth, 5)
        self.weights[1] = np.asarray(weights[self.weight_cnt[0]:]).reshape(self.depth)


#if __name__ == '__main__':
#    np.random.seed(None)
#    net = Network(6, 0.005)
#    net.randomizeWeights()
#    test = net.weights
#    p = net.run([200, 200, 3, 0.5, 200])
#    
#    g = net.getGenome()
#    net2 = Network(6, 0.005)
#    net2.randomizeWeights()
#    test2=net2.weights
#    g2 = net2.getGenome()
    
#    random_low = np.random.randint(0, len(g))
#    random_high = np.random.randint(0, len(g))
#    while random_low == random_high:
#        random_high = np.random.randint(0, len(g))
#    
#    if random_low > random_high:
#        random_low, random_high = random_high, random_low
#    
#    child = g[0:random_low] + g2[random_low:random_high] + g[random_high:]
#    net.updateWeights(child)
#    test = net.weights
#tester = np.random.randn(6, 5) / np.sqrt(5)
#print('tester: ', tester)
#tester = tester.flatten().tolist()
#print('flattened: ', tester)
#tester = np.asarray(tester).reshape(6, 5)
#print('reshaped: ', tester)



