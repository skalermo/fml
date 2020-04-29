import unittest
from Lexer.Lexer import TokenType
from Error import ErrorCode
from tests.parser.utils import should_fail


class TestIfStatementFails(unittest.TestCase):
    def test_lparen(self):
        s = 'if ) ;'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

    def test_empty_condition(self):
        s = 'if ();'
        should_fail(self, s, ErrorCode.EMPTY_COND)

        s = 'if ((((()))));'
        should_fail(self, s, ErrorCode.EMPTY_COND)

    def test_rparen(self):
        s = 'if (c ;'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_no_statement(self):
        s = 'if (c) else ;'
        should_fail(self, s, ErrorCode.EXPECTED_STATEMENT)

        s = 'if (c) else'
        should_fail(self, s, ErrorCode.EXPECTED_STATEMENT)

    def test_no_semi(self):
        s = 'if (c) expr'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)


if __name__ == '__main__':
    unittest.main()
