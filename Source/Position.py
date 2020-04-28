class Position:
    def __init__(self, source):
        self.line = source.line
        self.column = source.column
        self.pos = source.current_pos

    def __str__(self):
        return f'position=[{self.line}:{self.column}]'

    def __repr__(self):
        return self.__str__()



