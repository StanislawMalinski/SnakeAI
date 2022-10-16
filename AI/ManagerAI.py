
from pandas import read_csv
import matplotlib.pyplot as plt


from AI.AI_UI import AI_UI
from AI.DataFrameFileTranslator import get_weights_and_biases
from AI.NeuralNetwork import NeuralNetwork
from AI.ThreadAI import ThreadAI
from SnakeGame.Board import Board
from SnakeGame.Snake import Snake


class ManagerAI:
    def __init__(self, number_of_players_in_session, number_of_iteration, root=None):
        self.results = []
        best = None
        for iteration in range(number_of_iteration):
            scores = []
            threads = []
            for p in range(number_of_players_in_session):
                if root == None:
                    player = NeuralNetwork((120, 10, 10, 4))
                else:
                    if p == 0:
                        player = NeuralNetwork((120, 10, 10, 4), parent=root, noise=0)
                    else:
                        player = NeuralNetwork((120, 10, 10, 4), parent=root)
                board = Board(20, 20)
                ui = AI_UI(1000, 900, board, player)
                snake = Snake(board.get_field(10, 10), board, ui)
                #ui.updateWindow(snake)
                thread = ThreadAI(ui, snake, player)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
                scores.append([thread.snake.length, thread.player])
            best = scores[0]
            for df in scores:
                if best[0] < df[0]:
                    best = df
            print(best[0])
            self.results.append(best[0])
            root = best[1]


        df = best[1].toDataFrame()

        df.to_csv("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\BestOfIteration" + str(number_of_iteration) + ".csv")
'''
                df = player.toDataFrame()
                if os.path.exists("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\TMP" + str(p) + ".csv"):
                    os.remove("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\TMP" + str(p) + ".csv")

                f = open("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\TMP" + str(p) + ".csv", "x")

                df.to_csv("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\TMP" + str(p) + ".csv")
                scores.append(("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\TMP" + str(p) + ".csv", snake.length))
                '''

df = read_csv("C:\\Users\\Staszek\\PycharmProjects\\AISnake\\AI\\BestOfIteration1000.csv")

weights, biases = get_weights_and_biases(df)

net = NeuralNetwork(weights_of_the_layers=weights, biases_of_the_layer=biases)

man = ManagerAI(100, 1000, root=net)


plt.plot( range(len(man.results)),man.results)
plt.ylabel('length of snake')
plt.xlabel('iteration')

plt.show()

