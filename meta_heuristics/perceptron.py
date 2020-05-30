import math

import numpy as np


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Neuron(object):
    def __init__(self, value=0.0):
        # self.parents = []
        # self.children = []
        self.weights = {}
        self.value = value
        # self.activation = self.value

    def activate(self):
        s = 0
        for neuron in self.weights.keys():
            s += neuron.value * self.weights[neuron]
        self.value = sigmoid(s)

    def __str__(self):
        return "W = " + str(self.weights) + " and value = " + str(self.value)


class NeuralNet(object):
    def __init__(self):
        self.inputs = []
        self.layers = []
        self.outputs = []

    def forward(self):
        for layer in self.layers:
            layer.activate()
        for output in self.outputs:
            output.activate()

    def error(self, preds):
        error = 0
        for output in self.outputs:
            error += abs(output.value - preds)

        return error

    # def backward(self, preds):


if __name__ == '__main__':
    input1 = Neuron(0.1)
    input2 = Neuron(0.5)

    layer1 = Neuron()
    # layer1.parents.append(input1)
    # layer1.parents.append(input2)
    layer1.weights[input1] = 0
    layer1.weights[input2] = 0

    output1 = Neuron()
    # output1.value = 0.2
    output1.weights[layer1] = 0

    snn = NeuralNet()
    snn.inputs.append(input1)
    snn.inputs.append(input2)
    snn.layers.append(layer1)
    snn.outputs.append(output1)

    print(input1)
    print(input2)

    print("layer1 : " + str(layer1))

    print("output1 : " + str(output1))

    snn.forward()

    print(snn.error(0.2))

    print("layer1 : " + str(layer1))

    print("output1 : " + str(output1))


