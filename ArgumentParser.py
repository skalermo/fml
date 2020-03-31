from argparse import ArgumentParser


def parseArguments() -> vars:
    parser = ArgumentParser(prog='fmli.py', description='Fantastic Matrix Language Interpreter')
    parser.add_argument('filename', type=str, metavar='', help='File to interpret')
    args = vars(parser.parse_args())
    return args
