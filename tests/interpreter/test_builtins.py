import unittest
from tests.interpreter.utils import interpret, should_fail
from Error import ErrorCode


class TestBuiltins(unittest.TestCase):
    def test_print(self):
        import io
        from contextlib import redirect_stdout

        with io.StringIO() as buf, redirect_stdout(buf):
            s = 'a = [1, 2, 3, 4];' \
                'print(a);'
            interpret(s)
            self.assertEqual('[[1.0, 2.0, 3.0, 4.0]]\n', buf.getvalue())

        with io.StringIO() as buf, redirect_stdout(buf):
            s = 'print("Hello world!");'
            interpret(s)
            self.assertEqual('Hello world!\n', buf.getvalue())

        with io.StringIO() as buf, redirect_stdout(buf):
            s = 'a = "Hello world!";' \
                'print(a, a, a, a, a);'
            interpret(s)
            self.assertEqual('Hello world! '*4 + 'Hello world!\n', buf.getvalue())

    def test_print_too_many_parametrs(self):
        s = 'print(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);'
        should_fail(self, s, expected_error_code=ErrorCode.TOO_MANY_ARGUMENTS)

    def test_abs(self):
        s = 'a = -1;' \
            'ret abs(a);'
        self.assertEqual(1, interpret(s).to_py())

        s = 'a = 1;' \
            'ret abs(a);'
        self.assertEqual(1, interpret(s).to_py())

        s = 'a = [-1, -2];' \
            'abs(a);'
        should_fail(self, s,
                    expected_error_code=ErrorCode.UNSUPPORTED_TYPE_ABS)

        s = 'a = "string";' \
            'abs(a);'
        should_fail(self, s,
                    expected_error_code=ErrorCode.UNSUPPORTED_TYPE_ABS)

    def test_len(self):
        s = 'a = [];' \
            'ret len(a);'
        self.assertEqual(0, interpret(s).to_py())

        s = 'a = [1, 2, 3;' \
            '     4, 5, 6];' \
            'ret len(a);'
        self.assertEqual(6, interpret(s).to_py())

        s = 'ret len("Hello");'
        self.assertEqual(5, interpret(s).to_py())

        s = 'a = "Hello";' \
            'ret len(a);'
        self.assertEqual(5, interpret(s).to_py())

        s = 'a = 1;' \
            'ret len(a);'
        should_fail(self, s, expected_error_code=ErrorCode.SCALAR_LEN)

    def test_max(self):
        s = 'a = 1;' \
            'b = 3;' \
            'ret max(a, b);'
        self.assertEqual(3, interpret(s).to_py())

        s = 'ret max([], [1]);'
        self.assertEqual([[1]], interpret(s).to_py())

        s = 'a = "";' \
            'b = "a";' \
            'ret max(a, b);'
        self.assertEqual('a', interpret(s).to_py())

        s = 'max(1, []);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPES_MAX)

        s = 'a = "a";' \
            'max(1, a);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPES_MAX)

        s = 'a = "a";' \
            'max(a, []);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPES_MAX)

    def test_min(self):
        s = 'a = 1;' \
            'b = 3;' \
            'ret min(a, b);'
        self.assertEqual(1, interpret(s).to_py())

        s = 'ret min([1], [1, 2, 3]);'
        self.assertEqual([[1]], interpret(s).to_py())

        s = 'a = "";' \
            'b = "a";' \
            'ret min(a, b);'
        self.assertEqual('', interpret(s).to_py())

        s = 'min(1, []);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPES_MIN)

        s = 'a = "a";' \
            'min(1, a);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPES_MIN)

        s = 'a = "a";' \
            'min(a, []);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPES_MIN)

    def test_round(self):
        s = 'a = 4.5;' \
            'ret round(a);'
        self.assertEqual(round(4.5), interpret(s).to_py())

        s = 'a = 4.4;' \
            'ret round(a);'
        self.assertEqual(round(4.4), interpret(s).to_py())

        s = 'a = 4.8;' \
            'ret round(a);'
        self.assertEqual(round(4.8), interpret(s).to_py())

        s = 'a = 4.0;' \
            'ret round(a);'
        self.assertEqual(round(4.0), interpret(s).to_py())

        s = 'a = [1, 2; 3, 4];' \
            'ret round(a);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPE_ROUND)

        s = 'a = "a";' \
            'ret round(a);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPE_ROUND)

    def test_shape(self):
        s = 'ret shape([1, 2, 3; 4, 5, 6]);'
        self.assertEqual([[2, 3]], interpret(s).to_py())

        s = 'ret shape(shape([1]));'
        self.assertEqual([[1, 2]], interpret(s).to_py())

        s = 'shape(2);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPE_SHAPE)

        s = 'a = "a";' \
            'shape(a);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPE_SHAPE)

    def test_transpose(self):
        s = 'ret transpose([1, 2]);'
        self.assertEqual([[1], [2]], interpret(s).to_py())

        s = 'ret transpose([1; 2]);'
        self.assertEqual([[1, 2]], interpret(s).to_py())

        s = 'transpose(1);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPE_TRANSPOSE)

        s = 'a = "a";' \
            'transpose(a);'
        should_fail(self, s, expected_error_code=ErrorCode.UNSUPPORTED_TYPE_TRANSPOSE)


if __name__ == '__main__':
    unittest.main()
