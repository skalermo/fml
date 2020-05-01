from Interpreter.Ast import AST


class String(AST):
    def __init__(self, token_string):
        self.token_string = token_string

    def __repr__(self):
        return f'{self.__class__.__name__}'
