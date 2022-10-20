from time import sleep


class SnakeSegment:
    def __init__(self, counter, last_segment, field):
        self.counter = counter
        self.last_segment = last_segment
        self.field = field
        if counter > 0:
            self.field.setSomething(self)

    def addToCounter(self):
        self.counter += 1

    def tic(self):
        self.counter -= 1
        if self.counter == 0:
            self.field.removeAnything()


class Snake:
    def __init__(self, starting_field, board, UI):
        self.UI = UI
        self.alive = True
        self.length = 2
        self.last_segment = SnakeSegment(2, None, starting_field)
        self.last_direction = 0  # 0 -> right, 1 -> down, 2 -> left, 3 -> up
        self.field_of_head = starting_field
        self.board = board

    def setDirection(self, direction):
        if (self.last_direction - direction) % 4 == 2:
            return
        self.last_direction = direction

    def run(self):
        row = self.field_of_head.row
        col = self.field_of_head.col
        if self.last_direction == 0:
            if self.field_of_head.col + 1 >= self.board.columns:
                self.die()
            else:
                self.set_head_field(row, col + 1)
        elif self.last_direction == 1:
            if self.field_of_head.row + 1 >= self.board.rows:
                self.die()
            else:
                self.set_head_field(row + 1, col)
        elif self.last_direction == 2:
            if self.field_of_head.col - 1 < 0:
                self.die()
            else:
                self.set_head_field(row, col - 1)
        elif self.last_direction == 3:
            if self.field_of_head.row - 1 < 0:
                self.die()
            else:
                self.set_head_field(row - 1, col)
        segment = self.last_segment
        while segment is not None:
            segment.tic()
            segment = segment.last_segment

    def set_head_field(self, row, col):
        new_tile = self.board.get_field(row, col)

        if new_tile.contains_snake():
            self.die()
        elif new_tile.contains_apple():
            self.length += 1
            new_tile.removeAnything()
            self.board.add_apple()
            self.board.NonRepeatingCounter = 0
            segment = self.last_segment
            while segment is not None:
                segment.addToCounter()
                segment = segment.last_segment

        seg = SnakeSegment(self.length - 1, self.last_segment, self.field_of_head)

        new_tile.setSomething(self)

        self.last_segment = seg

        self.field_of_head = new_tile

    def die(self):
        self.UI.endGame(self)
