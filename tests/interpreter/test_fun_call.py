import unittest
from tests.interpreter.utils import interpret, should_fail
from Error import ErrorCode, ErrorDescription


class TestFunCall(unittest.TestCase):
    def test_call_with_return(self):
        s = 'fun some_function()' \
            '   ret 1;' \
            'ret some_function();'
        self.assertEqual(1, interpret(s).to_py())

    def test_fun_call_one_arg(self):
        s = 'fun a(b)' \
            '   ret b;' \
            'ret a(5);'
        self.assertEqual(5, interpret(s).to_py())

    def test_scopes(self):
        s = 'a = 0;' \
            'fun f(a)' \
            '   a = a + 1;' \
            'f(1);' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

        s = 'a = 0;' \
            'fun f(a)' \
            '   a = a + 1;' \
            'f(a);' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

        s = 'a = 0;' \
            'fun f(a)' \
            '   ret a + 1;' \
            'a = f(a);' \
            'ret a;'
        self.assertEqual(1, interpret(s).to_py())

    def test_fun_not_defined(self):
        s = 'f();'
        should_fail(self, s,
                    expected_error_code=ErrorCode.FUN_NOT_DEFINED,
                    expected_id='f')

        s = '{' \
            '   {' \
            '       f();' \
            '   }' \
            '}'
        should_fail(self, s,
                    expected_error_code=ErrorCode.FUN_NOT_DEFINED,
                    expected_id='f')

    def test_arguments_number_mismatch(self):
        s = 'fun f(a, b);' \
            'f(1);'
        should_fail(self, s,
                    expected_error_code=ErrorCode.NUMBER_OF_PARAMS_MISMATCH,
                    expected_id='f')

        s = 'fun f(a, b);' \
            'f(1, 2, 3);'
        should_fail(self, s,
                    expected_error_code=ErrorCode.NUMBER_OF_PARAMS_MISMATCH,
                    expected_id='f')

    def test_create_local_var(self):
        s = 'fun f()' \
            '   a = 1;' \
            'ret a;'
        should_fail(self, s,
                    expected_error_code=ErrorCode.ID_NOT_FOUND,
                    expected_id='a')

    def test_global_var_and_param(self):
        s = 'fun f(a) {' \
            '   a = 1;' \
            '}' \
            'a = 0;' \
            'f(1);' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

        s = 'a = 0;' \
            'fun f(a)' \
            '   a = 1;' \
            'f(1);' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

    def test_factorial(self):
        s = 'fun factorial(n) {' \
            '   if (n < 2)' \
            '       ret 1;' \
            '   else' \
            '       ret n * factorial(n-1);' \
            '}' \
            'ret factorial(10);'
        self.assertEqual(3628800, interpret(s).to_py())

    def test_recursion_depth(self):
        s = 'fun recursion(depth) {' \
            '   if (depth > 0) {' \
            '       depth = depth - 1;' \
            '       recursion(depth);' \
            '   }' \
            '}' \
            'recursion(100);'
        should_fail(self, s,
                    expected_error_code=ErrorCode.MAX_RECURSION_DEPTH_EXCEED,
                    expected_id='recursion')

        s = 'fun recursion(depth) {' \
            '   if (depth > 0) {' \
            '       depth = depth - 1;' \
            '       recursion(depth);' \
            '   }' \
            '}' \
            'recursion(99);'
        interpret(s)

    def test_string_as_argument(self):
        s = 'a = 0;' \
            'fun some_fun(s)' \
            '   a = s;' \
            'some_fun("Hello");' \
            'ret a;'
        self.assertEqual('Hello', interpret(s).to_py())


if __name__ == '__main__':
    unittest.main()
