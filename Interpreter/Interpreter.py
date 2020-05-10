from Interpreter.Ast import NodeVisitor
from Interpreter.Environment import Environment
from Objects.Scalar import Scalar
from Objects.Matrix import Matrix, MatrixRow
from Objects.String import String
from Error import InterpreterError
from Error import ErrorCode

# todo
# implement functions:
# abs, len, max, min, print, round, shape, transp


class ReturnException(Exception):
    def __init__(self, value):
        self.value_to_return = value


class Interpreter(NodeVisitor):
    def __init__(self):
        self.env = None
        self.operations = None

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
            '<': self.less,
            '>': self.greater,
            '<=': self.less_or_equal,
            '>=': self.greater_or_equal,
            '==': self.equal,
            '!=': self.not_equal,
            '**': self.pow
        }

    def interpret(self, program):
        return self.visit(program)

    def visit_Program(self, program):
        self.env = Environment()
        self.operations = self._get_binary_operations()

        try:
            for object in program.objects:
                self.visit(object)
        except ReturnException as re:
            return re.value_to_return
        return None

    def visit_FunctionDefinition(self, fun_def):
        self.env.add_fun_def(fun_def)

    def visit_ReturnStatement(self, ret_statement):
        value_to_return = self.visit(ret_statement.expression)
        raise ReturnException(value_to_return)

    def visit_ForLoop(self, for_loop):
        pass

    def visit_WhileLoop(self, while_loop):
        while self.visit(while_loop.condition_expression):
            self.visit(while_loop.statement)

    def visit_DoWhileLoop(self, do_while_loop):
        self.visit(do_while_loop.statement)
        while self.visit(do_while_loop.condition_expression):
            self.visit(do_while_loop.statement)

    def visit_CompoundStatement(self, comp_statement):
        for statement in comp_statement.statement_list:
            self.visit(statement)

    def visit_IfStatement(self, if_statement):
        if self.visit(if_statement.condition):
            self.visit(if_statement.statement)
        else:
            self.visit(if_statement.else_statement)

    def visit_EmptyStatement(self, empty_statement):
        return

    def visit_Assignment(self, assignment):
        rvalue = self.visit(assignment.rvalue)
        self.env.add_var(assignment.lvalue, rvalue)

    def visit_BinaryOperator(self, bin_op):
        lvalue = self.visit(bin_op.lvalue)
        op = bin_op.op
        rvalue = self.visit(bin_op.rvalue)

        return self.operations[op.value](lvalue, rvalue)

    def visit_UnaryOperator(self, unary_op):
        pass

    def visit_FunctionCall(self, fun_call):
        pass

    def visit_MatrixSubscripting(self, mtrx_subs):
        pass

    def visit_MatrixIndex(self, idx):
        pass

    def visit_Matrix(self, matrix):
        return matrix

    def visit_Identifier(self, id):
        if (value := self.env.get_var(id)) is None:
            self.error(error_code=ErrorCode.ID_NOT_FOUND, id=id.value)
        return value

    def visit_Scalar(self, scalar):
        return scalar

    def visit_String(self, string):
        return str

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
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(a.value + b.value)
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            if a.shape != b.shape:
                self.error(error_code=ErrorCode.MATRIX_SHAPE_MISMATCH,
                           description=f'{a.shape} != {b.shape}')
            return self.add_matrices(a, b)

        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Addition on {type(a)} and {type(b)}')

    def sub(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(a.value - b.value)
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            pass
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Subtraction on {type(a)} and {type(b)}')

    def mul(self, a, b):
        return a * b

    def float_division(self, a, b):
        return a / b

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

    # operations on matrices
    def add_matrices(self, a, b):
        # sum up elements on same positions
        # return new matrix

        # matrix is empty
        if not len(a):
            return a

        rows = []
        for row_of_a, row_of_b in zip(a.rows, b.rows):
            summed_elements = []
            for element_in_row_of_a, element_in_row_of_b in zip(row_of_a, row_of_b):
                summed_elements.append(self.add(element_in_row_of_a, element_in_row_of_b))
            rows.append(MatrixRow(summed_elements))
        return Matrix(rows)

    def error(self, error_code=None, id='', description=''):
        raise InterpreterError(error_code, id, description)
