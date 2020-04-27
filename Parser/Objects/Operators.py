class Evaluable:
    pass


class BinaryOperator(Evaluable):
    def __init__(self, lvalue, op, rvalue):
        self.lvalue = lvalue
        self.op = op
        self.rvalue = rvalue


class UnaryOperator(Evaluable):
    def __init__(self, op, rvalue):
        self.op = op
        self.rvalue = rvalue
