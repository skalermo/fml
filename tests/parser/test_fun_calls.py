import unittest
from Lexer.Token import TokenType
from Error import ErrorCode
from tests.parser.utils import should_fail


class TestFunCallFails(unittest.TestCase):
    def test_rparen(self):
        f = 'a('
        should_fail(self, f, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_no_second_arg(self):
        f = 'a(a, );'
        should_fail(self, f, ErrorCode.EXPECTED_EXPRESSION)

    def test_no_first_arg(self):
        f = 'a(, a);'
        should_fail(self, f, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)


if __name__ == '__main__':
    unittest.main()
