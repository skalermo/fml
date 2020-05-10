# This is python port of the clang TextTreeStructure class.
# Link to the original source below.
# https://clang.llvm.org/doxygen/TextNodeDumper_8h_source.html
#
#
# Thanks to Witold Wysota for provided simplified C++ source code.


from sys import stdout
from typing import List, Tuple, Callable


class TextTreeStructure:
    def __init__(self):
        self.pending: List[Tuple[Callable, str]] = []
        self.top_level = True
        self.first_child = True
        self.prefix: List[str] = []

    def add_child(self, do_add_child: Callable, label: str = ''):
        if self.top_level:
            self.top_level = False

            # print top level object
            stdout.write(label)

            do_add_child()

            while self.pending:
                self.dump_with_indent(True, *self.pending[-1])
                self.pending.pop()
            self.prefix = []
            stdout.write('\n')
            self.top_level = True
            return

        if self.first_child:
            self.pending.append((do_add_child, label,))
        else:
            self.dump_with_indent(False, *self.pending[-1])
            self.pending[-1] = (do_add_child, label,)
        self.first_child = False

    def dump_with_indent(self, is_last_child: bool, do_add_child: Callable, label: str):
        stdout.write('\n')
        # stdout.write(Colors.Blue)
        colored(Colors.Blue, '{prefix}{char}-'.format(
            prefix=''.join(self.prefix),
            char='`' if is_last_child else '|'
        ))
        if label:
            stdout.write(str(label))

        self.prefix.append(' ' if is_last_child else '|')
        self.prefix.append(' ')

        self.first_child = True
        depth = len(self.pending)
        do_add_child()

        while depth < len(self.pending):
            self.dump_with_indent(True, *self.pending[-1])
            self.pending.pop()
        self.prefix.pop()
        self.prefix.pop()


class Colors:
    Black = '\u001b[30m'
    Red = '\u001b[31m'
    Green = '\u001b[32m'
    Yellow = '\u001b[33m'
    Blue = '\u001b[34m'
    Magenta = '\u001b[35m'
    Cyan = '\u001b[36m'
    White = '\u001b[37m'

    Bright_Black = '\u001b[30;1m'
    Bright_Red = '\u001b[31;1m'
    Bright_Green = '\u001b[32;1m'
    Bright_Yellow = '\u001b[33;1m'
    Bright_Blue = '\u001b[34;1m'
    Bright_Magenta = '\u001b[35;1m'
    Bright_Cyan = '\u001b[36;1m'
    Bright_White = '\u001b[37;1m'

    Reset = '\u001b[0m'


def colored(color: str, text: str):
    stdout.write(f'{color}{text}{Colors.Reset}')
