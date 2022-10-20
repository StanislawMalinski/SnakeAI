import math

import numpy as np
from numpy import savetxt, matrix

from AI.DataFrameFileTranslator import get_df


def activation_f(x):
    return 1 / (1 + math.exp(-x))


class NeuralNetwork:
    def __init__(self, neuron_distribution_in_layers=(1, 1), data_frame=None, parent=None, noise=0, weights_of_the_layers=None, biases_of_the_layer=None):
        self.weights_of_the_layers = []
        self.biases_of_the_layer = []
        self.number_of_layers = len(neuron_distribution_in_layers) - 1
        self.size_of_input = neuron_distribution_in_layers[0]
        self.neuron_distribution_in_layers = neuron_distribution_in_layers

        self.score = 0

        if weights_of_the_layers is not None and biases_of_the_layer is not None:
            self.weights_of_the_layers = weights_of_the_layers
            self.biases_of_the_layer = biases_of_the_layer
            self.get_distribution()
            if noise > 0:
                for index in range(len(weights_of_the_layers)):
                    mat = self.weights_of_the_layers[index]
                    shape_w = mat.shape
                    noise_mat = np.matrix(np.random.random(shape_w) * noise - noise / 2)
                    res = mat + noise_mat
                    self.weights_of_the_layers[index] = res

                for index in range(len(biases_of_the_layer)):
                    mat = biases_of_the_layer[index]
                    shape_b = mat.shape
                    self.biases_of_the_layer[index] = np.add(mat, np.random.random(shape_b) * noise - noise / 2)
            return

        if parent is not None:
            for weights in parent.weights_of_the_layers:
                mat = weights.copy()
                shape_w = mat.shape
                noise_mat = np.matrix(np.random.random(shape_w) * noise - noise / 2)
                res = mat + noise_mat
                self.weights_of_the_layers.append(res)

            for biases in parent.biases_of_the_layer:
                mat = biases.copy()
                shape_b = mat.shape
                noise_mat = np.random.random(shape_b) * noise - noise / 2
                res = mat + noise_mat
                self.biases_of_the_layer.append(res)
            return

        if data_frame is None and parent is None and weights_of_the_layers is None and biases_of_the_layer is None:
            self.generate_random(neuron_distribution_in_layers)

    def generate_random(self, neuron_distribution_in_layers):
        for i in range(self.number_of_layers + 1):
            if i == 0:
                input_layer = np.random.rand(neuron_distribution_in_layers[i], 1)
            else:
                weights = np.matrix(
                    -1 + 2 * np.random.rand(neuron_distribution_in_layers[i - 1], neuron_distribution_in_layers[i]))
                biases = np.matrix(-1 + 2 * np.random.rand(1, neuron_distribution_in_layers[i]))
                self.weights_of_the_layers.append(weights)
                self.biases_of_the_layer.append(biases)

    def evaluate_at(self, X):
        row, col = X.shape
        if col != self.size_of_input:
            print("Wrong size input!")

        for i in range(self.number_of_layers):
            X = np.dot(X, self.weights_of_the_layers[i])
            X += self.biases_of_the_layer[i]
            X = X.tolist()
            X = np.matrix([[activation_f(cell) for cell in row] for row in X])

        return X

    def toDataFrame(self):
        return get_df(self.weights_of_the_layers, self.biases_of_the_layer)

    def get_distribution(self):
        distribution = []
        counter = 0
        for layer in self.weights_of_the_layers:
            for neuron in layer:
                counter += 1
            distribution.append(counter)
            counter = 0
        self.neuron_distribution_in_layers = distribution
