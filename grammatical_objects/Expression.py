class Expression:
    pass


class ConditionExpression(Expression):
    # OrExpression
    pass


class Assignment(Expression):
    def __init__(self, lhs: str, rhs: [str, ConditionExpression]):
        self.lhs = lhs
        self.rhs = rhs


class AndExpression:
    pass


class EqualitySubExpression:
    pass


class RelativeExpression:
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
