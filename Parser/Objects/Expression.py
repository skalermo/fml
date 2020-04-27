class Expression:
    pass


class MultitermExpression(Expression):
    def __init__(self, subexpressions, used_operators=None):
        self.subexpressions = subexpressions
        self.operators = used_operators


class ConditionExpression(MultitermExpression):
    # OrExpression
    pass


class Assignment:
    def __init__(self, lhs, rhs):
        # rhs: Identifier or ConditionalExpression
        self.lhs = lhs
        self.rhs = rhs


class AndExpression(MultitermExpression):
    pass


class EqualityExpression(MultitermExpression):
    pass


class RelativeExpression(MultitermExpression):
    pass


class ArithmeticExpression(MultitermExpression):
    pass


class Term(MultitermExpression):
    pass


class MiniTerm(Expression):
    def __init__(self, unary_operator, microterm):
        self.unary_operator = unary_operator
        self.microterm = microterm


class MicroTerm(Expression):
    def __init__(self, base, power):
        self.base = base
        self.power = power


class Factor(Expression):
    pass















