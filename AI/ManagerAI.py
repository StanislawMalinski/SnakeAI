from pandas import read_csv
import matplotlib.pyplot as plt

from AI.AI_UI import AI_UI
from AI.DataFrameFileTranslator import get_weights_and_biases
from AI.NeuralNetwork import NeuralNetwork
from AI.ThreadAI import ThreadAI
from SnakeGame.Board import Board
from SnakeGame.Snake import Snake


def to_str_arr(arr):
    n_arr = []
    for el in arr:
        n_arr.append(str(el))
    return n_arr


class ManagerAI:
    def __init__(self, number_of_players_in_session, number_of_iteration, root=None):
        self.results = []
        self.best = None
        distribution = (240, 80, 80, 4)
        for iteration in range(number_of_iteration):
            threads = []
            if root is None:
                root = NeuralNetwork(distribution)
            for p in range(number_of_players_in_session):
                if p == 0:
                    player = NeuralNetwork(distribution, parent=root)
                else:
                    player = NeuralNetwork(distribution, parent=root, noise=0.1)
                board = Board(20, 20)
                ui = AI_UI(1000, 900, board, player)
                snake = Snake(board.get_field(10, 10), board, ui)
                thread = ThreadAI(ui, snake, player)
                thread.start()
                threads.append(thread)
                #ui.updateWindow(snake)
                #scores.append([snake.length, player])

            self.best = threads[0]
            for el in threads:
                el.join()
                score = el.snake.length - 2
                if self.best.snake.length - 2 < score:
                    self.best = el
            print("Best out of batch: " + str(self.best.snake.length - 2))
            self.results = self.best.snake.length - 2
            root = self.best.player

        df = self.best.player.toDataFrame()

        df.to_csv(
            "C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\BestOfIteration10.csv")


result = []

df = read_csv("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\BestOfIteration10.csv")

weights, biases = get_weights_and_biases(df)

net = NeuralNetwork(weights_of_the_layers=weights, biases_of_the_layer=biases)

#net = NeuralNetwork((240, 80, 80, 4))

while True:
    simulation = ManagerAI(10, 10, root=net)

    net = simulation.best.player

    df = net.toDataFrame()

    df.to_csv("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\BestOfIteration10.csv")