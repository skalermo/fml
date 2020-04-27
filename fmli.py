from Lexer.Lexer import Lexer
from Source.Source import StringSource


def main():
    # args = parseArguments()
    # filename = args['filename']
    # file_source = FileSource(filename)
    # lexer = Lexer(file_source)
    # token = lexer.build_next_token()
    # while token:
    #     print(token)
    #     token = lexer.build_next_token()
    string = '...'
    source = StringSource(string)
    Lexer(source)


if __name__ == '__main__':
    main()
