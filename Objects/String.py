from Interpreter.Ast import AST


class String(AST):
    def __init__(self, string):
        self.value = string

    def __repr__(self):
        return f'{self.__class__.__name__}'
