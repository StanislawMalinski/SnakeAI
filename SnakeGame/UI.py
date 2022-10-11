import pygame
import math

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


    def updateWindow(self,snake):
        clock = pygame.time.Clock()
        FPS = 2
        while self.running:
            clock.tick(FPS)
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
            pygame.display.update()

    def getVertices(self,x_top_left, y_top_left,side_length):

        return [[x_top_left, y_top_left], [x_top_left + side_length, y_top_left],
                    [x_top_left + side_length, y_top_left + side_length], [x_top_left, y_top_left + side_length]]

    def drawSquare(self, x_top_left, y_top_left, side_length, color):
        vertices = self.getVertices(x_top_left,y_top_left,side_length)
        pygame.draw.polygon(self.screen, color, vertices)

    def get_coordinates(self, row, column, x_center, y_center):
        x_pivot = x_center - (self.board.rows*(self.side_length + self.margin))/2
        y_pivot = y_center - (self.board.cols*(self.side_length + self.margin))/2
        top_left_x = column * (self.side_length + self.margin)
        top_left_y = row * (self.side_length + self.margin)
        return x_pivot + top_left_x, y_pivot + top_left_y

    def drawBoard(self, board):
        for field in board.fields:
            top_left_x, top_left_y = self.get_coordinates(field.row, field.col)
            field.setGraphic(self)
            self.drawSquare(top_left_x, top_left_y, self.side_length, (190,190,190))
