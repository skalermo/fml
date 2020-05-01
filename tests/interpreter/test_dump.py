import unittest
from Parser.Parser import Parser
from Lexer.Lexer import Lexer
from Source.Source import StringSource
from Interpreter.AstDumper import AstDumper


class TestAstDumper(unittest.TestCase):
    def test_something(self):
        string_source = '{' \
                        'a(1+3);' \
                        'b(2+4);' \
                        'c(5+6);' \
                        '}'
        parser = Parser(Lexer(StringSource(string_source)))
        program = parser.parse_program()
        ast_dumper = AstDumper()
        ast_dumper.add_child(lambda: ast_dumper.visit(program), str(program))


if __name__ == '__main__':
    unittest.main()
