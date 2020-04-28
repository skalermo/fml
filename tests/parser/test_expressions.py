import unittest
from Source.Source import StringSource
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Error import ParserError, ErrorCode


class TestExpressionsFails(unittest.TestCase):
    @staticmethod
    def should_fail(tester, expression, expected_error_code=None):
        parser = Parser(Lexer(StringSource(expression)))
        with tester.assertRaises(ParserError) as e:
            parser.parse_program()
        if expected_error_code is not None:
            tester.assertEqual(expected_error_code, e.exception.error_code)

    def test_rvalue_or_expr(self):
        expr = '-3 + 3 or;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

    def test_rvalue_and_expr(self):
        expr = 'a + a- b ' \
               'and;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

    def test_rvalue_eq_expr(self):
        expr = '-5 == 2;' \
               '3 ==;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = 'b != a;' \
               'b != ;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

    def test_rvalue_relativ_expr(self):
        expr = '-4 <;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = 'a >=;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = 'c <=;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = 'a >;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

    def test_rvalue_aexpr(self):
        expr = '-3 + 3 + +;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = '- a -;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = '-;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

    def test_rvalue_term(self):
        expr = 'a * b *;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = 'a - b div 5; b div;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = '80 mod b; 6 mod;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

        expr = 'b / a / b / a / b /;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)

    def test_rvalue_microterm(self):
        expr = 'a = b **;'
        TestExpressionsFails.should_fail(self, expr, ErrorCode.RVAL_FAIL)





if __name__ == '__main__':
    unittest.main()
