from Interpreter.Ast import AST


class Identifier(AST):
    def __init__(self, token):
        self.value = token.value
        self.position = token.position

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def get_name(self):
        return self.value
