import unittest
from tests.interpreter.utils import interpret, should_fail
from Error import ErrorCode, ErrorDescription


class TestIfStatement(unittest.TestCase):
    def test_true_condition(self):
        s = 'a = 0;' \
            'if (1>0)' \
            '   a = 1;' \
            'ret a;'
        self.assertEqual(1, interpret(s).to_py())

    def test_false_condition(self):
        s = 'a = 0;' \
            'if (1<0)' \
            '   a = 1;' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

    def test_variable_in_condition(self):
        s = 'a = 0;' \
            'if (2*a+1 > 3)' \
            '   a = 1;' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

    def test_else_statement(self):
        s = 'a = 0;' \
            'if (1<0)' \
            '   ;' \
            'else' \
            '   a = a - 1;' \
            'ret a;'
        self.assertEqual(-1, interpret(s).to_py())

    def test_nested_if_statements(self):
        s = 'a = 40;' \
            'b = 0;' \
            'if (a > 18)' \
            '   if (a < 48)' \
            '       b = 1;' \
            '   else' \
            '       b = 2;' \
            'else' \
            '   b = 3;' \
            'ret b;'
        self.assertEqual(1, interpret(s).to_py())

        s = 'a = 50;' \
            'b = 0;' \
            'if (a > 18)' \
            '   if (a < 48)' \
            '       b = 1;' \
            '   else' \
            '       b = 2;' \
            'else' \
            '   b = 3;' \
            'ret b;'
        self.assertEqual(2, interpret(s).to_py())

        s = 'a = 18;' \
            'b = 0;' \
            'if (a > 18)' \
            '   if (a < 48)' \
            '       b = 1;' \
            '   else' \
            '       b = 2;' \
            'else' \
            '   b = 3;' \
            'ret b;'
        self.assertEqual(3, interpret(s).to_py())

    def test_else_scope(self):
        s = 'a = 50;' \
            'b = 0;' \
            'if (a > 18) {' \
            '   if (a < 48)' \
            '       b = 1;' \
            '}' \
            'else' \
            '   b = 3;' \
            'ret b;'
        self.assertEqual(0, interpret(s).to_py())


if __name__ == '__main__':
    unittest.main()
