from Interpreter.Ast import AST


class Identifier(AST):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.token.value}'
