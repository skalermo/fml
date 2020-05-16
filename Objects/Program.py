from Interpreter.Ast import AST


class Program(AST):
    def __init__(self, objects):
        self.objects = objects

    def __repr__(self):
        return f'{self.__class__.__name__}'
