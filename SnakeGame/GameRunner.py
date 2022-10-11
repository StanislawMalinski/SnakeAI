import pygame

from SnakeGame.Board import Board
from SnakeGame.Snake import Snake
from SnakeGame.UI import UI

if __name__ == '__main__':
    screenWidth = 1000
    screenHeight = 800
    pygame.init()
    board = Board()
    ui = UI(screenWidth, screenHeight,board)
    ui.drawBoard(board)
    snake = Snake(board.get_field(10,10),board)
    ui.updateWindow(snake)