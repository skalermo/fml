class Evaluable:
    pass


class Expression(Evaluable):
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


class FunctionCall(Expression):
    def __init__(self, id, argument_list):
        self.id = id
        self.argument_list = argument_list


class Identifier(Expression):
    def __init__(self, id):
        self.id = id


class MatrixSubscripting(Expression):
    def __init__(self, id, idx, idx2):
        self.id = id
        self.row_index = idx
        self.column_index = idx2


class MatrixIndex:
    def __init__(self, expression, is_full_index=False):
        self.expression = expression
        self.is_full_index = is_full_index


class String:
    def __init__(self, token):
        self.token = token
