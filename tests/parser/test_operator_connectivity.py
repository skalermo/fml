import unittest
from Parser.Parser import Parser
from Source.Source import StringSource
from Objects.Operators import BinaryOperator
from Objects.Identifier import Identifier
from Lexer.Token import Token, TokenType
from Objects.Scalar import Scalar


def create_expected_binary_operator(parameters):
    binop = None
    actions = {
        'scalar': lambda value: Scalar(Token(TokenType.SCALAR, value)),
        'op': lambda type: Token(TokenType(type)),
        'id': lambda id: Identifier(Token(Token(TokenType.ID, id))),
        'prev': lambda _: binop
    }

    for param in parameters:
        binop = BinaryOperator(
            lvalue=actions[param[0][0]](param[0][1]),
            op=actions[param[1][0]](param[1][1]),
            rvalue=actions[param[2][0]](param[2][1])
        )

    return binop


class TestOperatorConnectivity(unittest.TestCase):
    def visit_and_compare(self, expected, actual):
        self.assertEqual(type(expected), type(actual))
        method = 'visit_and_compare_' + actual.__class__.__name__
        visitor = getattr(self, method)
        return visitor(expected, actual)

    def visit_and_compare_BinaryOperator(self, expected, actual):
        self.assertEqual(expected.op.type, actual.op.type)

        self.visit_and_compare(expected.lvalue, actual.lvalue)
        self.visit_and_compare(expected.rvalue, actual.rvalue)

    def visit_and_compare_Identifier(self, expected, actual):
        self.assertEqual(expected.token.value, actual.token.value)

    def visit_and_compare_Scalar(self, expected, actual):
        self.assertEqual(expected.token.value, actual.token.value)

    def test_assignment_expression(self):
        source = 'a=b=c=0;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'c',), ('op', '=',), ('scalar', 0.0,)),
             (('id', 'b',), ('op', '=',), ('prev', None,)),
             (('id', 'a',), ('op', '=',), ('prev', None,))]
        )
        self.visit_and_compare(expected, actual)

    def test_condition_expression(self):
        source = 'a or b or c or 0;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', 'or',), ('id', 'b',)),
             (('prev', None,), ('op', 'or',), ('id', 'c',)),
             (('prev', None,), ('op', 'or',), ('scalar', 0.0,))]
        )
        self.visit_and_compare(expected, actual)

    def test_and_expression(self):
        source = 'a and b and c and 0;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', 'and',), ('id', 'b',)),
             (('prev', None,), ('op', 'and',), ('id', 'c',)),
             (('prev', None,), ('op', 'and',), ('scalar', 0.0,))]
        )
        self.visit_and_compare(expected, actual)

    def test_equality_expression(self):
        source = 'a == b != c == 0;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', '==',), ('id', 'b',)),
             (('prev', None,), ('op', '!=',), ('id', 'c',)),
             (('prev', None,), ('op', '==',), ('scalar', 0.0,))]
        )
        self.visit_and_compare(expected, actual)

    def test_relative_expression(self):
        source = 'a >= b > c < d <= 0;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', '>=',), ('id', 'b',)),
             (('prev', None,), ('op', '>',), ('id', 'c',)),
             (('prev', None,), ('op', '<',), ('id', 'd',)),
             (('prev', None,), ('op', '<=',), ('scalar', 0.0,))]
        )
        self.visit_and_compare(expected, actual)

    def test_arithmetic_expression(self):
        source = 'a+b-c+d+5-4-7+4+3;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', '+',), ('id', 'b',)),
             (('prev', None,), ('op', '-',), ('id', 'c',)),
             (('prev', None,), ('op', '+',), ('id', 'd',)),
             (('prev', None,), ('op', '+',), ('scalar', 5.0,)),
             (('prev', None,), ('op', '-',), ('scalar', 4.0,)),
             (('prev', None,), ('op', '-',), ('scalar', 7.0,)),
             (('prev', None,), ('op', '+',), ('scalar', 4.0,)),
             (('prev', None,), ('op', '+',), ('scalar', 3.0,))]
        )
        self.visit_and_compare(expected, actual)

    def test_term(self):
        source = 'a mod b / c div d * 0;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', 'mod',), ('id', 'b',)),
             (('prev', None,), ('op', '/',), ('id', 'c',)),
             (('prev', None,), ('op', 'div',), ('id', 'd',)),
             (('prev', None,), ('op', '*',), ('scalar', 0.0,))]
        )
        self.visit_and_compare(expected, actual)

    def test_microterm(self):
        source = 'a**b;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('id', 'a',), ('op', '**',), ('id', 'b',))]
        )
        self.visit_and_compare(expected, actual)

        source = '5**4.5;'
        program = Parser(StringSource(source)).parse_program()
        actual = program.objects[0]
        expected = create_expected_binary_operator(
            [(('scalar', 5.0,), ('op', '**',), ('scalar', 4.5,))]
        )
        self.visit_and_compare(expected, actual)


if __name__ == '__main__':
    unittest.main()
