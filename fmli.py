from argparse import ArgumentParser
from Source.Source import FileSource
from Interpreter.AstDumper import dumpAST


def parseArguments() -> vars:
    parser = ArgumentParser(prog='fmli.py', description='Fantastic Matrix Language Interpreter')
    parser.add_argument('filename', type=str, metavar='filename', help='File to interpret')
    parser.add_argument('-d', '--dump', action='store_true', default=False, help='Dump AST of provided source')
    return vars(parser.parse_args())


def main():
    args = parseArguments()
    print(args)
    if args['dump']:
        source = FileSource(args['filename'])
        dumpAST(source)


if __name__ == '__main__':
    main()
