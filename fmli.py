from argparse import ArgumentParser
from Source.Source import FileSource
from Interpreter.AstDumper import dumpAST
from Interpreter.Interpreter import Interpreter


def parseArguments() -> vars:
    parser = ArgumentParser(prog='fmli.py', description='Fantastic Matrix Language Interpreter')
    parser.add_argument('filename', type=str, metavar='filename', help='File to interpret')
    parser.add_argument('-d', '--dump', action='store_true', default=False, help='Dump AST of provided source')
    return vars(parser.parse_args())


def main():
    args = parseArguments()
    source = FileSource(args['filename'])
    if args['dump']:
        dumpAST(source)
        return

    Interpreter(source).interpret()


if __name__ == '__main__':
    main()
