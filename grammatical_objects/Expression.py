from Token import TokenType


class Expression:
    def __init__(self, subexpressions, used_operators):
        self.subexpressions = subexpressions
        self.operators = used_operators


class ConditionExpression(Expression):
    # OrExpression
    pass


class Assignment:
    def __init__(self, lhs: str, rhs: [str, ConditionExpression]):
        self.lhs = lhs
        self.rhs = rhs


class AndExpression:
    pass


class EqualityExpression:
    pass


class RelativeExpression:
    pass


class ArithmeticExpression:
    pass


class Term:
    pass


class MiniTerm:
    def __init__(self, unary_operator, microterm):
        self.unary_operator = unary_operator
        self.microterm = microterm


# This dictionary structure:
#   ExpressionClass(key) -> [SubExpressionClass, [Operators]](value)
#   'SubExpression' is a term of 'Expression'. It is also the next key in the dict.
#   'Operators' are possible to encounter operators in each expression.
subexpressions_and_binary_operators = {
        ConditionExpression: [
            AndExpression,
            [TokenType.OR]
        ],
        AndExpression: [
            EqualityExpression,
            [TokenType.AND]
        ],
        EqualityExpression: [
            RelativeExpression,
            [TokenType.EQ, TokenType.NEQ]
        ],
        RelativeExpression: [
            ArithmeticExpression,
            [TokenType.LEQ, TokenType.LESS,
             TokenType.GEQ, TokenType.GRE]
        ],
        ArithmeticExpression: [
            Term,
            [TokenType.PLUS, TokenType.MINUS]
        ],
        Term: [
            MiniTerm,
            [TokenType.MUL, TokenType.FLOAT_DIV,
             TokenType.INTEGER_DIV, TokenType.MODULO]
        ],
        MiniTerm: None
    }


class MicroTerm:
    pass


class Factor:
    pass


class FunctionCall:
    pass


class MatrixSubscripting:
    pass
