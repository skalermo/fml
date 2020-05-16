import unittest
from Lexer.Lexer import TokenType
from Error import ErrorCode, ErrorDescription
from tests.parser.utils import should_fail


class TestIfStatementFails(unittest.TestCase):
    def test_lparen(self):
        s = 'if ) ;'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

    def test_empty_condition(self):
        s = 'if ();'
        should_fail(self, s,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_IF_CONDITION)

        s = 'if ((((()))));'
        should_fail(self, s,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_IF_CONDITION)

    def test_rparen(self):
        s = 'if (c ;'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_no_statement(self):
        s = 'if (c) else ;'
        should_fail(self, s,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_IF_BODY)

        s = 'if (c) expr; else'
        should_fail(self, s,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_ELSE_BODY)

    def test_no_semi(self):
        s = 'if (c) expr'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)


if __name__ == '__main__':
    unittest.main()
