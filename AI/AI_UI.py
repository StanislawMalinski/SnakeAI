import math
import random
import time

import numpy
import pygame


class AI_UI:

    def __init__(self, windowWidth, windowHeight, board, network):
        self.backgroundColor = (80, 80, 80)
        self.tileColor = (190, 190, 190)
        self.resourcesColor = (0, 160, 0)
        self.hatcheryColor = (150, 45, 45)

        self.width = windowWidth
        self.height = windowHeight

        self.board = board
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake AI")
        self.screen.fill(self.backgroundColor)

        self.side_length = 25
        self.margin = 3

        self.network = network

        self.define_x_y_of_the_field()

        self.drawBoard(board)

    def updateWindow(self, snake):
        counter = 0
        self.board.add_apple()
        while self.running:
            counter += 1
            self.drawBoard(self.board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            input_matrix = self.get_input_matrix(snake.field_of_head)
            result = self.network.evaluate_at(input_matrix)
            choice = self.interpret_result(result)

            snake.setDirection(choice)

            snake.run()

            pygame.display.update()

    def get_input_matrix(self, field_of_head):
        row = field_of_head.row
        col = field_of_head.col

        result = []

        for x in range(-5, 6):
            for y in range(-5, 6):
                if x == y == 0:
                    continue

                if x + col < 0 or x + col >= self.board.rows or y + row < 0 or y + row >= self.board.rows:
                    result.append(0)
                    continue

                field = self.board.get_field(x+col, y+row)

                if field.contains_apple():
                    result.append(1)
                elif field.contains_snake():
                    result.append(0.8)
                else:
                    result.append(0.2)

        return numpy.matrix(result)

    def interpret_result(self, result):
        sum = 0
        list = result.tolist()
        list = list[0]

        for res in list:
            sum += math.exp(res)
        interpreted = []

        for res in list:
            interpreted.append(math.exp(res) / sum)

        choice = random.random()
        sum = 0

        for threshold_index in range(len(interpreted)):
            sum += interpreted[threshold_index]
            if choice < sum:
                return threshold_index
        return len(interpreted) - 1

    def getVertices(self, x_top_left, y_top_left):

        return [[x_top_left, y_top_left],
                [x_top_left + self.side_length, y_top_left],
                [x_top_left + self.side_length, y_top_left + self.side_length],
                [x_top_left, y_top_left + self.side_length]]

    def drawSquare(self, x_top_left, y_top_left, color):
        vertices = self.getVertices(x_top_left, y_top_left)
        pygame.draw.polygon(self.screen, color, vertices)

    def get_coordinates(self, row, column):
        x_pivot = self.width / 2 - (self.board.rows * (self.side_length + self.margin)) / 2
        y_pivot = self.height / 2 - (self.board.columns * (self.side_length + self.margin)) / 2
        top_left_x = column * (self.side_length + self.margin)
        top_left_y = row * (self.side_length + self.margin)
        return x_pivot + top_left_x, y_pivot + top_left_y

    def define_x_y_of_the_field(self):
        for field in self.board.fields:
            field.x, field.y = self.get_coordinates(field.row, field.col)

    def drawBoard(self, board):
        for field in board.fields:
            self.drawSquare(field.x, field.y, field.color)

    def endGame(self, snake):
        self.network.score = snake.length
        self.running = False
