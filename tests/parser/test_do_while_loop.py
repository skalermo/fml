import unittest
import unittest
from Lexer.Token import TokenType
from Error import ErrorCode
from tests.parser.utils import should_fail


class TestDoWhileFails(unittest.TestCase):
    def test_loop_no_statement(self):
        # actually pretty interesting
        # breaks here          V
        loop = 'do while (1>0); '
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.WHILE)

        loop = 'do fun function(a, b);'
        should_fail(self, loop, ErrorCode.EXPECTED_STATEMENT)

    def test_loop_no_while_token(self):
        loop = 'do {;};'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.WHILE)

        loop = 'do {1+3; 1+4; a= b= c = 4+2-6;}'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.WHILE)

    def test_loop_no_parentheses(self):
        loop = 'do {;} while 1>0;'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

        loop = 'do {;} while (1>0;'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_loop_no_semi_at_end(self):
        loop = 'do ; while (1)'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)


if __name__ == '__main__':
    unittest.main()
