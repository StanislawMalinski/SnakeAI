import pygame

from SnakeGame.Apple import Apple
from SnakeGame.Snake import Snake, SnakeSegment


class Field:
    def __init__(self, row, col):
        self.UI = None
        self.row = row
        self.col = col
        self.contains = 0

    def setSomething(self, thing):
        self.contains = thing
        if isinstance(thing, Snake) or isinstance(thing, SnakeSegment):
            color = (0, 240, 100)
        elif isinstance(thing, Apple):
            color = (200, 0, 0)
        else:
            color = (190, 190, 190)
        pygame.draw.polygon(self.UI.screen, color, self.UI.getVertices())

    def removeAnything(self):
        self.contains = 0
        pygame.draw.polygon(self.UI.screen, (190, 190, 190), self.UI.vertices)

    def setGraphic(self, UI):
        self.UI = UI


class Board:
    def __init__(self):
        self.fields = []
        self.rows = 20
        self.columns = 20

        for row in range(self.rows):
            for column in range(self.columns):
                self.fields.append(Field(row, column))

    def get_field(self, row, col):
        return self.fields[row*self.columns + col]

