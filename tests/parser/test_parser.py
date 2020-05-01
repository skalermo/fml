import unittest
from Source.Source import FileSource
from Parser.Parser import Parser
from Lexer.Lexer import Lexer


class ParserTest(unittest.TestCase):
    def test_fun_defs(self):
        filename = 'fun_defs.txt'
        src = FileSource(filename)
        lexer = Lexer(src)
        parser = Parser(lexer)
        parser.parse_program()


if __name__ == '__main__':
    unittest.main()
