import unittest
from Parser.Parser import Parser
from Source.Source import StringSource, FileSource
from Interpreter.AstDumper import AstDumper


class TestAstDumper(unittest.TestCase):
    def test_something(self):
        string_source = 'i = 100;\n' \
                        'while (a>1){\n' \
                        '   print(a-1);};'

        parser = Parser(StringSource(string_source))
        program = parser.parse_program()
        ast_dumper = AstDumper()
        ast_dumper.add_child(lambda: ast_dumper.visit(program), str(program))

    def test_filesource(self):
        filesource = FileSource('test.txt')
        parser = Parser(filesource)
        program = parser.parse_program()
        ast_dumper = AstDumper()
        ast_dumper.add_child(lambda: ast_dumper.visit(program), str(program))

    def test_fix_dump(self):
        s = 'a = 0;'
        parser = Parser(StringSource(s))
        program = parser.parse_program()
        ast_dumper = AstDumper()
        ast_dumper.add_child(lambda: ast_dumper.visit(program), str(program))


if __name__ == '__main__':
    unittest.main()
