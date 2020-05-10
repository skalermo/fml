import unittest
from Lexer.Token import TokenType
from Error import ErrorCode
from tests.parser.utils import should_fail
from Parser.Parser import Parser
from Source.Source import StringSource
from Objects.Operators import Assignment


class TestAssignmentFails(unittest.TestCase):
    def test_assign(self):
        a = 'var = 0;'
        self.assertTrue(isinstance(Parser(StringSource(a))
                                   .try_to_parse_expression(), Assignment))

    def test_no_id_assign(self):
        a = '1 = []'
        should_fail(self, a, ErrorCode.ASSIGNTONOTID)

    def test_nested_assign_no_id(self):
        a = 'var1 = var2 = 2 = var3 = 0;'
        should_fail(self, a, ErrorCode.ASSIGNTONOTID)


if __name__ == '__main__':
    unittest.main()
