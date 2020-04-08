import unittest
from Lexer import Lexer
from Token import TokenType
from Source import FileSource
from Error import LexerError


class LexerTest(unittest.TestCase):
    def test_easy_expressions(self):
        file_source = FileSource('expressions/easy.txt')
        lexer = Lexer(file_source)
        while lexer.current_token.type != TokenType.ETX:
            print(lexer.current_token)
            lexer.move_to_next_token()

    # def test_moderate_expressions(self):
    #     with open('expressions/moderate.txt') as file:
    #         lexer = Lexer(file.read())
    #
    #     current_token = lexer.move_to_next_token()
    #     print(current_token)
    #     while current_token.type != TokenType.EOF:
    #         print(current_token)
    #         current_token = lexer.move_to_next_token()

        # lexer = Lexer('3.')
        # with self.assertRaises(LexerError) as context:
        #     lexer.move_to_next_token()


if __name__ == '__main__':
    unittest.main()
