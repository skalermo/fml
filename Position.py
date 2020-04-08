class PositionBuilder:
    def __init__(self, source):
        self._source = source

    def current_position(self):
        return Position(self._source)


class Position:
    def __init__(self, source):
        self.line = source.line
        self.column = source.column
        # self._pos = source.pos

    def __str__(self):
        return f'position=[{self.line}:{self.column}]'

    def __repr__(self):
        return self.__str__()



