import unittest
from Parser.Parser import Parser
from Lexer.Lexer import Lexer
from Source.Source import StringSource
from Interpreter.AstDumper import AstDumper


class TestAstDumper(unittest.TestCase):
    def test_something(self):
        string_source = '   fun partition(arr, low, high)' \
                        '   {' \
                        '       i = (low -1);' \
                        '       pivot = arr[high];' \
                        '       for (j in range)' \
                        '           if (arr[j] < pivot)' \
                        '           {' \
                        '               i = i+1;' \
                        '               temp = arr[i];' \
                        '               arr[i] = arr[j];' \
                        '               arr[j] = temp;' \
                        '           }' \
                        '       temp = arr[i+1];' \
                        '       arr[i+1] = arr[high];' \
                        '       arr[high] = temp;' \
                        '       ret (i+1);' \
                        '   }' \
                        '   fun quickSort(arr, low, high)' \
                        '       if (low < high)' \
                        '       {' \
                        '           pi = partition(arr, low, high);' \
                        '           quickSort(arr, low, pi-1);' \
                        '           quickSort(arr, pi+1, high);' \
                        '       }'

        s = 'x[2];\n' \
            'a[1, 2];\n' \
            'b[a];\n' \
            'c[:];\n' \
            'd[:, 1];\n' \
            'e[1, :];\n' \
            'f[:, :];'

        parser = Parser(Lexer(StringSource(string_source)))
        program = parser.parse_program()
        ast_dumper = AstDumper()
        ast_dumper.add_child(lambda: ast_dumper.visit(program), str(program))


if __name__ == '__main__':
    unittest.main()
