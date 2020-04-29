import unittest
from Lexer.Token import TokenType
from Error import ErrorCode
from tests.parser.utils import should_fail


class TestForLoopFails(unittest.TestCase):
    def test_no_parentheses_on_condition(self):
        loop = 'for i in [a, b, c] ;'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

        loop = 'for (i in [a, b, c];'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_no_iterator(self):
        loop = 'for (in [a, b, c]);'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.ID)

    def test_in_keyword(self):
        loop = 'for (i [a, b, c ,]);'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.IN)

    def test_no_iterable(self):
        loop = 'for (i in );'
        should_fail(self, loop, ErrorCode.EXPECTED_ITERABLE)

    def test_no_rparen(self):
        loop = 'for (i in [a, b, c];'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)



if __name__ == '__main__':
    unittest.main()
