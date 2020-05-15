import unittest
from tests.interpreter.utils import interpret, should_fail
from Error import ErrorCode, ErrorDescription


class TestScope(unittest.TestCase):
    def test_global_id_not_found(self):
        s = 'a = 0;' \
            'ret a + b;'
        should_fail(self, s,
                    expected_error_code=ErrorCode.ID_NOT_FOUND,
                    expected_id='b')

    def test_local_scope(self):
        s = 'a = 32;' \
            '{' \
            '   ret a;' \
            '}'
        self.assertEqual(32, interpret(s).to_py())

    def test_local_scope_id_not_found(self):
        s = 'a = 32;' \
            '{' \
            '   ret b;' \
            '}'
        should_fail(self, s,
                    expected_error_code=ErrorCode.ID_NOT_FOUND,
                    expected_id='b')

    def test_change_global_var_inside_local_scope(self):
        s = 'a = 32;' \
            '{' \
            '   a = 0;' \
            '}' \
            'ret a;'
        self.assertNotEqual(32, interpret(s).to_py())
        self.assertEqual(0, interpret(s).to_py())

    def test_change_global_var_inside_nested_local_scope(self):
        s = 'a = 22;' \
            '{' \
            '   b = 0;' \
            '   {' \
            '       a = 0;' \
            '       b = 1;' \
            '       {' \
            '           a = b;' \
            '       }' \
            '       a = a + 2;' \
            '   }' \
            '   a = a + b;' \
            '}' \
            'ret a;'
        self.assertEqual(4, interpret(s).to_py())

    def test_nested_scopes_id_not_found(self):
        s = 'a = 1;' \
            '{' \
            '   b = 2;' \
            '   {' \
            '       c = 3;' \
            '       d = a + b + c;' \
            '   }' \
            '   d = a + b;' \
            '}' \
            'ret d;'
        should_fail(self, s,
                    expected_error_code=ErrorCode.ID_NOT_FOUND,
                    expected_id='d')


if __name__ == '__main__':
    unittest.main()
