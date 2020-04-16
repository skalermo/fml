class Expression:
    pass


class LogicalExpression(Expression):
    pass


class Assignment(Expression):
    def __init__(self, lhs: str, rhs: [str, LogicalExpression]):
        self.lhs = lhs
        self.rhs = rhs


class LogicalSubExpression:
    pass


class EqualitySubExpression:
    pass


class ComparisonExpression:
    pass


class ArithmeticExpression:
    pass


class Term:
    pass


class MiniTerm:
    pass


class MicroTerm:
    pass


class Factor:
    pass


class FunctionCall:
    pass


class MatrixSubscripting:
    pass
