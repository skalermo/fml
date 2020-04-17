from Token import TokenType


class Expression:
    def __init__(self, subexpressions, used_operators=None):
        self.subexpressions = subexpressions
        self.operators = used_operators


class ConditionExpression(Expression):
    # OrExpression
    pass


class Assignment:
    def __init__(self, lhs: str, rhs: [str, ConditionExpression]):
        self.lhs = lhs
        self.rhs = rhs


class AndExpression(Expression):
    pass


class EqualityExpression(Expression):
    pass


class RelativeExpression(Expression):
    pass


class ArithmeticExpression(Expression):
    pass


class Term(Expression):
    pass


class MiniTerm:
    def __init__(self, unary_operator, microterm):
        self.unary_operator = unary_operator
        self.microterm = microterm

class MicroTerm:
    def __init__(self, base, power):
        self.base = base
        self.power = power

class Factor:
    pass


class FunctionCall:
    def __init__(self, id, argument_list):
        self.id = id
        self.argument_list = argument_list


class Identifier:
    def __init__(self, id):
        self.id = id


class MatrixSubscripting:
    def __init__(self, id, idx, idx2):
        self.id = id
        self.row_index = idx
        self.column_index = idx2


class MatrixIndex:
    def __init__(self, expression, is_full_index=False):
        self.expression = expression
        self.is_full_index = is_full_index
