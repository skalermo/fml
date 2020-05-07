import unittest
from Lexer.Lexer import TokenType
from Error import ErrorCode, ErrorDescription
from tests.parser.utils import should_fail


class TestRetStatementFails(unittest.TestCase):
    def test_empty_expression(self):
        r = 'ret ;'
        should_fail(self, r,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_RET_BODY)

    def test_semi_missing(self):
        r = 'ret a'
        should_fail(self, r, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)

    def test_return_another_ret_statement(self):
        # try_to_parse_ret_statement fails to build statement
        # so it returns none, so there is no expression
        r = 'ret ret a;'
        should_fail(self, r,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_RET_BODY)


if __name__ == '__main__':
    unittest.main()
