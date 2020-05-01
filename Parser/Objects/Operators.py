from Interpreter.Ast import AST


class Evaluable(AST):
    def __repr__(self):
        raise NotImplementedError


class BinaryOperator(Evaluable):
    def __init__(self, lvalue, op, rvalue):
        self.lvalue = lvalue
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op.value}'


class UnaryOperator(Evaluable):
    def __init__(self, op, rvalue):
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op.value}'
