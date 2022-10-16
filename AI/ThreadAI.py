import threading


class ThreadAI(threading.Thread):
    def __init__(self, ui, snake, player):
        threading.Thread.__init__(self)
        self.ui = ui
        self.snake = snake
        self.player = player

    def run(self):
        self.ui.updateWindow(self.snake)