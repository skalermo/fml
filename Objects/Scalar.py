from Interpreter.Ast import AST


class Scalar(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def get_value(self):
        return self.value
