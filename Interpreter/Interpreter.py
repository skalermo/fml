from Interpreter.Ast import NodeVisitor
from Interpreter.Environment import Environment
from Lexer.Token import TokenType

# todo
# implement functions:
# abs, len, max, min, print, round, shape, transp


class Interpreter(NodeVisitor):
    def __init__(self):
        self.env = Environment()
        self.operations = self._get_binary_operations()

    def _get_binary_operations(self):
        return {
            'and': self.logic_and,
            'div': self.int_division,
            'mod': self.modulo,
            'or': self.logic_or,
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.float_division,
            '=': self.assign,
            '<': self.less,
            '>': self.greater,
            '<=': self.less_or_equal,
            '>=': self.greater_or_equal,
            '==': self.equal,
            '!=': self.not_equal,
            '**': self.pow
        }

    def interpret(self, object):
        self.visit(object)

    def visit_Program(self, program):
        for object in program.objects:
            self.visit(object)

    def visit_FunctionDefinition(self, fun_def):
        self.env.add_fun_def(fun_def)

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
        lvalue = self.visit(bin_op.lvalue)
        op = bin_op.op
        rvalue = bin_op.rvalue

        return self.operations[op](lvalue, rvalue)

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

    # binary operations

    def logic_and(self, a, b):
        return a or b

    def int_division(self, a, b):
        return a // b

    def modulo(self, a, b):
        return a % b

    def logic_or(self, a, b):
        return a or b

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def float_division(self, a, b):
        return a / b

    def assign(self, a, b):
        pass

    def less(self, a, b):
        pass

    def greater(self, a, b):
        pass

    def less_or_equal(self, a, b):
        pass

    def greater_or_equal(self, a, b):
        pass

    def equal(self, a, b):
        pass

    def not_equal(self, a, b):
        pass

    def pow(self, a, b):
        pass
