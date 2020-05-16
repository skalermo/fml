import unittest
from Lexer.Token import TokenType
from Error import ErrorCode, ErrorDescription
from tests.parser.utils import should_fail


class TestWhileLoopFails(unittest.TestCase):
    def test_loop_without_condition(self):
        loop = 'while {a + b;}'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

        loop = 'while 2>1 {a + b;}'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.LPAREN)

    def test_loop_without_rparen(self):
        loop = 'while (a < 2 {a + b;}'
        should_fail(self, loop, ErrorCode.UNEXPECTED_TOKEN, TokenType.RPAREN)

    def test_loop_no_statement(self):
        loop = 'while (1>0)'
        should_fail(self, loop,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_WHILE_BODY)

        loop = 'while (1>0){}'
        should_fail(self, loop,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_COMPOUND_STATEMENT)

    def test_loop_empty_condition(self):
        loop = 'while () 1+2;'
        should_fail(self, loop,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_WHILE_CONDITION)

        loop = 'while (()) 1+2;'
        should_fail(self, loop,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_WHILE_CONDITION)

        loop = 'while ((())) 1+2;'
        should_fail(self, loop,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_WHILE_CONDITION)


if __name__ == '__main__':
    unittest.main()
