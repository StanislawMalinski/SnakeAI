import random

import pygame

from SnakeGame.Apple import Apple
from SnakeGame.Snake import Snake, SnakeSegment


class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.contains = None
        self.color = (190, 190, 190)

    def hasSomething(self):
        return self.contains is not None

    def contains_apple(self):
        return isinstance(self.contains, Apple)

    def contains_snake(self):
        return isinstance(self.contains, SnakeSegment)
    def setSomething(self, thing):
        self.contains = thing
        if isinstance(thing, Snake) or isinstance(thing, SnakeSegment):
            self.color = (0, 240, 100)
        elif isinstance(thing, Apple):
            self.color = (200, 0, 0)
        else:
            self.color = (190, 190, 190)

    def removeAnything(self):
        self.contains = None
        self.color = (190, 190, 190)


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

    def add_apple(self):
        field = self.get_field_for_apple()
        field.setSomething(Apple(field))
    def get_field_for_apple(self):
        for i in range(10):
            generated = random.randint(0, len(self.fields))
            if not self.fields[generated].hasSomething():
                return self.fields[generated]

        for field in self.fields:
            if not field.hasSomething():
                return field
        return None