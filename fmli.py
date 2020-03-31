from Lexer import Lexer
from ArgumentParser import parseArguments


def main():
    args = parseArguments()
    file = args['filename']
    with open(file) as text:
        lexer = Lexer(text)


if __name__ == '__main__':
    main()
