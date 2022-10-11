
class Apple:
    def __init__(self, runner, field):
        self.runner = runner
        self.field = field

    def eat_me(self):
        self.runner.removeMe()
        self.field.removeApple()