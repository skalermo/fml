from sys import stdout
from Interpreter.Ast import NodeVisitor, AST


def colored(color, text):
    stdout.write(f'{color}{text}{Colors.Reset}')


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


class AstDumper(NodeVisitor):
    def __init__(self):
        self.pending = []
        self.top_level = True
        self.first_child = True
        self.prefix = []

    def add_child(self, do_add_child, label=''):
        if self.top_level:
            self.top_level = False

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

    def dump_with_indent(self, is_last_child, do_add_child, label):
        stdout.write('\n')
        stdout.write(Colors.Blue)
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

    def visit_Program(self, program):
        for object in program.objects:
            self.add_child(lambda object=object: self.visit(object), object)

    def visit_FunctionDefinition(self, fun_def):
        for parameter in fun_def.parameter_list:
            self.add_child(lambda parameter=parameter: self.visit(parameter), parameter)
        self.add_child(lambda: self.visit(fun_def.statement), fun_def.statement)

    def visit_ReturnStatement(self, ret_statement):
        self.add_child(lambda: self.visit(ret_statement.expression), ret_statement.expression)

    def visit_ForLoop(self, for_loop):
        self.add_child(lambda: self.visit(for_loop.iterator), for_loop.iterator)
        self.add_child(lambda: self.visit(for_loop.iterable), for_loop.iterable)
        self.add_child(lambda: self.visit(for_loop.statement), for_loop.statement)

    def visit_WhileLoop(self, while_loop):
        self.add_child(lambda: self.visit(while_loop.condition_expression),
                       while_loop.condition_expression)
        self.add_child(lambda: self.visit(while_loop.statement),
                       while_loop.statement)

    def visit_DoWhileLoop(self, do_while_loop):
        self.add_child(lambda: self.visit(do_while_loop.statement),
                       do_while_loop.statement)
        self.add_child(lambda: self.visit(do_while_loop.condition_expression),
                       do_while_loop.condition_expression)

    def visit_CompoundStatement(self, comp_statement):
        for statement in comp_statement.statement_list:
            self.add_child(lambda statement=statement: self.visit(statement), statement)

    def visit_IfStatement(self, if_statement):
        self.add_child(lambda: self.visit(if_statement.condition_expression),
                       if_statement.condition_expression)
        self.add_child(lambda: self.visit(if_statement.statement), if_statement.statement)
        if if_statement.else_statement is not None:
            self.add_child(lambda: self.visit(if_statement.else_statement),
                           if_statement.else_statement)

    def visit_BinaryOperator(self, bin_op):
        self.add_child(lambda: self.visit(bin_op.lvalue), bin_op.lvalue)
        self.add_child(lambda: self.visit(bin_op.rvalue), bin_op.rvalue)

    def visit_UnaryOperator(self, unary_op):
        self.add_child(lambda: self.visit(unary_op.rvalue), unary_op.rvalue)

    def visit_FunctionCall(self, fun_call):
        for argument in fun_call.argument_list:
            self.add_child(lambda argument=argument: self.visit(argument), argument)

    def visit_Matrix(self, matrix):
        pass

    def visit_Identifier(self, id):
        pass

    def visit_Scalar(self, scalar):
        pass

    def visit_EmptyStatement(self, empty_statement):
        pass

    def visit_String(self, string):
        pass






