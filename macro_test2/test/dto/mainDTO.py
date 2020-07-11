from pygments.lexer import this


class mainDTO():
    index = ''
    action = ''

    def __init__(self):
        global index
        global action

    def get_action(self):
        pass

    def set_action(self):
        pass

    def get_index(self):
        return globals(index)

    def set_index(self, idx):
        global index
        index = idx

    pass
