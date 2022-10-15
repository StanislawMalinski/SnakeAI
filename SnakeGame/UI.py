import pygame
import math

from pygame import QUIT

from SnakeGame.Board import Board
from SnakeGame.Snake import Snake


class UI:

    def __init__(self, windowWidth, windowHeight, board):
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

        self.define_x_y_of_the_field()


    def updateWindow(self,snake):
        clock = pygame.time.Clock()
        FPS = 60
        counter = 0
        while self.running:
            counter += 1
            clock.tick(FPS)
            self.drawBoard(self.board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                snake.setDirection(0)
            if keys[pygame.K_DOWN]:
                snake.setDirection(1)
            if keys[pygame.K_LEFT]:
                snake.setDirection(2)
            if keys[pygame.K_UP]:
                snake.setDirection(3)

            if counter % 5 == 0:
                snake.run()
            pygame.display.update()

    def getVertices(self, x_top_left, y_top_left):

        return [[x_top_left, y_top_left],
                [x_top_left + self.side_length, y_top_left],
                [x_top_left + self.side_length, y_top_left + self.side_length],
                [x_top_left, y_top_left + self.side_length]]

    def drawSquare(self, x_top_left, y_top_left, color):
        vertices = self.getVertices(x_top_left,y_top_left)
        pygame.draw.polygon(self.screen, color, vertices)

    def get_coordinates(self, row, column):
        x_pivot = self.width/2 - (self.board.rows*(self.side_length + self.margin))/2
        y_pivot = self.height/2 - (self.board.columns*(self.side_length + self.margin))/2
        top_left_x = column * (self.side_length + self.margin)
        top_left_y = row * (self.side_length + self.margin)
        return x_pivot + top_left_x, y_pivot + top_left_y

    def define_x_y_of_the_field(self):
        for field in self.board.fields:
            field.x, field.y = self.get_coordinates(field.row, field.col)

    def drawBoard(self, board):
        for field in board.fields:
            self.drawSquare(field.x, field.y, field.color)

    def endGame(self):
        self.running = False
        pygame.event.post(pygame.event.Event(pygame.QUIT))