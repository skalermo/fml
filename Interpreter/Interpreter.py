from Interpreter.Ast import NodeVisitor

# todo
# implement functions:
# abs, len, max, min, print, round, shape, transp


class Interpreter(NodeVisitor):
    def __init__(self):
        pass

    def interpret(self, object):
        self.visit(object)

    def visit_Program(self, program):
        pass

    def visit_FunctionDefinition(self, fun_def):
        pass

    def visit_ReturnStatement(self, ret_statement):
        pass

    def visit_ForLoop(self, for_loop):
        pass

    def visit_WhileLoop(self, while_loop):
        pass

    def visit_DoWhileLoop(self, do_while_loop):
        pass

    def visit_CompoundStatement(self, comp_statement):
        pass

    def visit_IfStatement(self, if_statement):
        pass

    def visit_EmptyStatement(self, empty_statement):
        pass

    def visit_BinaryOperator(self, bin_op):
        pass

    def visit_UnaryOperator(self, unary_op):
        pass

    def visit_FunctionCall(self, fun_call):
        pass

    def visit_MatrixSubscripting(self, mtrx_subs):
        pass

    def visit_MatrixIndex(self, idx):
        pass

    def visit_Matrix(self, matrix):
        pass

    def visit_Identifier(self, id):
        pass

    def visit_Scalar(self, scalar):
        pass

    def visit_String(self, string):
        pass
