import unittest
from tests.interpreter.utils import interpret, should_fail
from Error import ErrorCode


class TestForLoop(unittest.TestCase):
    def test_simple(self):
        s = 'sum = 0;' \
            'for (i in [1, 2, 3]) {' \
            '   #print(i);' \
            '   sum = sum + i;' \
            '}' \
            'ret sum;'
        self.assertEqual(6, interpret(s).to_py())

    def test_string(self):
        s = 'a = "Hello world!";' \
            'for (i in a);' \
            '   #print(i);'
        interpret(s)

    def test_scalar(self):
        s = 'a = 1;' \
            'for (i in a)' \
            '   print(i);'
        should_fail(self, s, expected_error_code=ErrorCode.NOT_ITERABLE)


if __name__ == '__main__':
    unittest.main()
