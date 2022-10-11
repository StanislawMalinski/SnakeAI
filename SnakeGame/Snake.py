from time import sleep

class SnakeSegment:
    def __init__(self, counter, last_segment, field):
        self.counter = counter
        self.last_segment = last_segment
        if counter > 0:
            self.field = field
            self.field.setSomething(self)
        
    def addToCounter(self):
        self.counter += 1
        if self.last_segment is not None:
            self.last_segment.addToCounter()
            
    def tic(self):
        self.counter += -1
        if self.counter == 0:
            self.field.removeSnake()
  

class Snake:
    def __init__(self, starting_field, board):
        self.alive = True
        self.length = 1
        self.last_segment = 0
        self.last_direction = [0]   # 0 -> right, 1 -> down, 2 -> left, 3 -> up
        self.field_of_head = starting_field
        self.field_of_head.setSomething(starting_field)
        self.board = board
        self.run()

    def setDirection(self, direction):
        self.last_direction = direction

    def run(self):
        row = self.field_of_head.row
        col = self.field_of_head.col
        if self.last_direction == 0:
            if self.field_of_head.col > self.board.columns:
                self.die()
            else:
                self.set_head_field(row, col+1)
        elif self.last_direction == 1:
            if self.field_of_head.row > self.board.rows:
                self.die()
            else:
                self.set_head_field(row+1, col)
        elif self.last_direction == 2:
            if self.field_of_head.col < 0:
                self.die()
            else:
                self.set_head_field(row, col-1)
        elif self.last_direction == 3:
            if self.field_of_head.row < 0:
                self.die()
            else:
                self.set_head_field(row-1, col)

    def set_head_field(self, row, col):
        if self.length > 1:
            self.field_of_head.setSomething(SnakeSegment(self.length-1, self.last_segment, self.field_of_head))
        self.field_of_head = self.board.get_field(row, col)
        self.board.get_field(row, col).setSomething(self)

    def die(self):
        self.board.endGame()
            