import unittest
from Error import ErrorCode
from tests.parser.utils import should_fail


class TestExpressionsFails(unittest.TestCase):
    def test_rvalue_assignment(self):
        expr = 'a =;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_or_expr(self):
        expr = '-3 + 3 or;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_and_expr(self):
        expr = 'a + a- b ' \
               'and;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_eq_expr(self):
        expr = '-5 == 2;' \
               '3 ==;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'b != a;' \
               'b != ;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_relativ_expr(self):
        expr = '-4 <;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'a >=;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'c <=;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'a >;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_aexpr(self):
        expr = '-3 + 3 + +;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = '- a -;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = '-;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_term(self):
        expr = 'a * b *;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'a - b div 5; b div;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = '80 mod b; 6 mod;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'b / a / b / a / b /;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_rvalue_microterm(self):
        expr = 'a = b **;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

    def test_unary_operators(self):
        expr = ' -;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'not;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = '+;'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = 'not ();'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)

        expr = '(- );'
        should_fail(self, expr, ErrorCode.EXPECTED_RVALUE)


if __name__ == '__main__':
    unittest.main()
