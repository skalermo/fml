from sys import stdout
from typing import Callable


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TextTreeStructure:
    def __init__(self):
        self.Pending = [Callable[[bool], None]]
        self.TopLevel: bool = True
        self.FirstChild: bool = True
        self.Prefix: str = ""

    def DumpWithIndent(self, IsLastChild: bool, DoAddChild: Callable, LabelStr: str):
        stdout.write('\n')

        stdout.write('{color_symbol}{prefix}{char}-'.format(
            color_symbol={bcolors.OKBLUE},
            prefix=self.Prefix,
            char='`' if IsLastChild else '|'
        ))
        if len(LabelStr):
            stdout.write(f'{LabelStr}: ')
        stdout.write(bcolors.ENDC)
        self.Prefix = ''.join([self.Prefix, ' ' if IsLastChild else '|'])
        self.Prefix = ''.join([self.Prefix, ' '])

        self.FirstChild = True
        # current depth
        Depth = len(self.Pending)

        DoAddChild()
        # depth might have changed (increased)

        while Depth < len(self.Pending):
            self.Pending[-1](True)
            self.Pending.pop()
        self.Prefix = self.Prefix[:-2]

    def AddChild(self, DoAddChild: Callable, Label: str = ""):
        # if top level
        if self.TopLevel:
            self.TopLevel = False
            DoAddChild()  # do stuff
            # if there is something in backlog...
            while len(self.Pending):
                self.Pending[-1](True)  # execute the last one
                self.Pending.pop()

            self.Prefix = ""
            stdout.write('\n')
            self.TopLevel = True
            return

        LabelStr = Label
        DumpWithIndent = lambda IsLastChild, DoAddChild=DoAddChild, LabelStr=LabelStr: \
            self.DumpWithIndent(IsLastChild, DoAddChild, LabelStr)

        if self.FirstChild:
            self.Pending.append(DumpWithIndent)
        else:
            self.Pending[-1](False)
            self.Pending[-1] = DumpWithIndent
        self.FirstChild = False

#
# def visit(self, node):
#     AddChild(lambda node=node: DoAddChild(node))
#
#
# def DoAddChild(node):
#     stdout.write(f'Node {node.test}')
#     if len(node.args):
#         stdout.write(f': {node.args}')
#
