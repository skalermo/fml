from Interpreter.Ast import AST


class Scalar(AST):
    def __init__(self, token):
        self.token = token
        self.position = token.position

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.token.value}'
