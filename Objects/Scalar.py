from Interpreter.Ast import AST


class Scalar(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def __bool__(self):
        if self.value == 0:
            return False
        return True

    def __eq__(self, other):
        return self.value == other.value

    def get_value(self):
        return self.value
