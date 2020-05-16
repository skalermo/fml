import unittest
from Lexer.Lexer import TokenType
from Error import ErrorCode, ErrorDescription
from tests.parser.utils import should_fail


class TestFunDefsFails(unittest.TestCase):
    def test_def_without_id(self):
        fun_def = 'fun () {;}'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.ID)

    def test_def_without_parentheses(self):
        fun_def = 'fun some_function 1+2;'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

        fun_def = 'fun some_function (a, b;'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_def_params_no_comma(self):
        fun_def = 'fun some_function (a b);'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

        fun_def = 'fun some_function (a + b);'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_def_no_statement(self):
        fun_def = 'fun some_function()'
        should_fail(self, fun_def,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_FUN_BODY)

        fun_def = 'fun some_function(){}'
        should_fail(self, fun_def,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_COMPOUND_STATEMENT)

        fun_def = 'fun some_function(){{;}{}}'
        should_fail(self, fun_def,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_COMPOUND_STATEMENT)

    def test_def_no_parameters_but_comma(self):
        fun_def = 'fun some_function(a, );'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.ID)

        fun_def = 'fun some_function(a, b, );'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.ID)

        fun_def = 'fun some_function(, );'
        should_fail(self, fun_def,
                    ErrorCode.UNEXPECTED_TOKEN, TokenType.ID)


if __name__ == '__main__':
    unittest.main()
