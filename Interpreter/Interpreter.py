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

MAX_RECURSION_DEPTH = 100


class ReturnException(Exception):
    def __init__(self, value):
        self.value_to_return = value


class Interpreter(NodeVisitor):
    def __init__(self):
        self.env = None
        self.binary_operations = None
        self.unary_operations = None

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

    def _get_unary_operations(self):
        return {
            'not': self.negation,
            '+': self.unary_plus,
            '-': self.unary_minus
        }

    def find_var(self, id):
        if (found := self.env.get_var(id)) is None:
            self.error(error_code=ErrorCode.ID_NOT_FOUND, id=id)
        return found

    def interpret(self, program):
        return self.visit(program)

    def visit_Program(self, program):
        self.env = Environment()
        self.binary_operations = self._get_binary_operations()
        self.unary_operations = self._get_unary_operations()

        try:
            for object in program.objects:
                self.visit(object)
        except ReturnException as re:
            return re.value_to_return
        return Scalar(0)

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
        self.env.create_new_local_scope()
        for statement in comp_statement.statement_list:
            self.visit(statement)
        self.env.destroy_local_scope()

    def visit_IfStatement(self, if_statement):
        if self.visit(if_statement.condition_expression):
            self.visit(if_statement.statement)
        elif if_statement.else_statement is not None:
            self.visit(if_statement.else_statement)

    def visit_EmptyStatement(self, empty_statement):
        return

    def visit_Assignment(self, assignment):
        rvalue = self.visit(assignment.rvalue)
        self.env.set_var(assignment.lvalue, rvalue)

    def visit_BinaryOperator(self, bin_op):
        lvalue = self.visit(bin_op.lvalue)
        op = bin_op.op
        rvalue = self.visit(bin_op.rvalue)

        return self.binary_operations[op.value](lvalue, rvalue)

    def visit_UnaryOperator(self, unary_op):
        rvalue = self.visit(unary_op.rvalue)
        op = unary_op.op
        return self.unary_operations[op.value](rvalue)

    def visit_FunctionCall(self, fun_call):
        if (fun_def := self.env.get_fun_def(fun_call.id)) is None:
            self.error(error_code=ErrorCode.FUN_NOT_DEFINED,
                       description=f'Function id: {fun_call.id.get_name()}',
                       id=fun_call.id.get_name())

        to_return = Scalar(0)
        arguments = []
        for arg in fun_call.argument_list:
            arguments.append(self.visit(arg))

        if len(arguments) != len(fun_def.parameter_list):
            self.error(error_code=ErrorCode.NUMBER_OF_PARAMS_MISMATCH,
                       description=f'Function {fun_def.id.get_name()} '
                                   f'takes {len(fun_def.parameter_list)} parameters, '
                                   f'got {len(arguments)} instead',
                       id=fun_def.id.get_name())

        if self.env.fun_call_nesting >= MAX_RECURSION_DEPTH:
            self.error(error_code=ErrorCode.MAX_RECURSION_DEPTH_EXCEED,
                       id=fun_def.id.get_name())

        self.env.create_new_fun_scope(fun_def.parameter_list, arguments)

        try:
            self.visit(fun_def.statement)
        except ReturnException as re:
            to_return = re.value_to_return

        self.env.destroy_fun_scope()
        return to_return

    def visit_MatrixSubscripting(self, mtrx_subs):
        matrix = self.find_var(mtrx_subs.id)
        row_idx = self.visit(mtrx_subs.row_index)
        column_idx = None if mtrx_subs.column_index is None \
            else self.visit(mtrx_subs.column_index)

        if isinstance(row_idx, Scalar) and not row_idx.value.is_integer():
            self.error(error_code=ErrorCode.FLOAT_IDX,
                       description=f'Row index of matrix {mtrx_subs.id}')
        if isinstance(column_idx, Scalar) and not column_idx.value.is_integer():
            self.error(error_code=ErrorCode.FLOAT_IDX,
                       description=f'Column index of matrix {mtrx_subs.id}')

        if row_idx is not None and column_idx is not None:
            if row_idx == 'colon' and column_idx == 'colon':
                return matrix.copy()

            if row_idx == 'colon':
                if (column := matrix.get_column(int(column_idx.to_py()))) is None:
                    self.error(error_code=ErrorCode.COLUMN_INDEX_OUT_OF_RANGE)
                return column

            if column_idx == 'colon':
                if (row := matrix.get_row(int(row_idx.to_py()))) is None:
                    self.error(error_code=ErrorCode.ROW_INDEX_OUT_OF_RANGE)
                return row

            if (row := matrix[int(row_idx.to_py())]) is None:
                self.error(error_code=ErrorCode.ROW_INDEX_OUT_OF_RANGE,
                           description=f'Row index {int(row_idx.to_py())}'
                                       f' in matrix {mtrx_subs.id}')
            if (item := row[int(column_idx.to_py())]) is None:
                self.error(error_code=ErrorCode.COLUMN_INDEX_OUT_OF_RANGE,
                           description=f'Column index {int(column_idx.to_py())}'
                                       f' in matrix {mtrx_subs.id}')
            return item

        if row_idx is not None:
            if row_idx == 'colon':
                return matrix.copy()
            if (item := matrix.get_item_by_single_idx(int(row_idx.to_py()))) is None:
                self.error(error_code=ErrorCode.OUT_OF_RANGE,
                           description=f'Index {int(row_idx.to_py())}'
                                       f' in matrix {mtrx_subs.id}')
            return item

    def visit_MatrixIndex(self, idx):
        if idx.is_colon:
            return 'colon'
        return self.visit(idx.expression)

    def visit_Matrix(self, matrix):
        for i in range(len(matrix.rows)):
            matrix[i] = self.visit(matrix[i])
        return matrix

    def visit_MatrixRow(self, row):
        for i in range(len(row)):
            row[i] = self.visit(row[i])
        return row

    def visit_Identifier(self, id):
        if (value := self.env.get_var(id)) is None:
            self.error(error_code=ErrorCode.ID_NOT_FOUND, id=id.value)
        return value

    def visit_Scalar(self, scalar):
        return scalar

    def visit_String(self, string):
        return string

    # binary operations

    def logic_and(self, a, b):
        return Scalar(int(a and b))

    def int_division(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            if b.value == 0:
                self.error(error_code=ErrorCode.ZERO_DIVISION)
            return Scalar(a.value // b.value)
        return self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                          description=f'Addition on {type(a)} and {type(b)}')

    def modulo(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            if b.value == 0:
                self.error(error_code=ErrorCode.ZERO_DIVISION)
            return Scalar(a.value % b.value)
        return self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                          description=f'Addition on {type(a)} and {type(b)}')

    def float_division(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            if b.value == 0:
                self.error(error_code=ErrorCode.ZERO_DIVISION)
            return Scalar(a.value / b.value)
        return self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                          description=f'Addition on {type(a)} and {type(b)}')

    def negation(self, a):
        return Scalar(int(not a))

    def unary_plus(self, a):
        if isinstance(a, String):
            self.error(error_code=ErrorCode.UNSUPPORTED_UNARY_OPERATION,
                       description=f'Type == String')
        return a

    def unary_minus(self, a):
        if isinstance(a, String):
            self.error(error_code=ErrorCode.UNSUPPORTED_UNARY_OPERATION,
                       description=f'Type == String')
        if isinstance(a, Scalar):
            a.value = -a.value
        if isinstance(a, Matrix):
            a = self.mul(a, Scalar(-1))
        return a

    def logic_or(self, a, b):
        return Scalar(int(a or b))

    def add(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(a.value + b.value)
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            if a.shape != b.shape:
                self.error(error_code=ErrorCode.MATRIX_SHAPE_MISMATCH,
                           description=f'{a.shape} != {b.shape}')
            return self.for_each_element_do(self.add, a, b)
        if isinstance(a, Matrix) and isinstance(b, Scalar):
            return self.for_each_element_do(self.add, a, b)

        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Addition on {type(a)} and {type(b)}')

    def sub(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(a.value - b.value)
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            if a.shape != b.shape:
                self.error(error_code=ErrorCode.MATRIX_SHAPE_MISMATCH,
                           description=f'{a.shape} != {b.shape}')
            return self.for_each_element_do(self.sub, a, b)
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Subtraction on {type(a)} and {type(b)}')

    def mul(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(a.value * b.value)
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            if a.shape[1] != b.shape[0]:
                self.error(error_code=ErrorCode.MATRIX_DOT_SHAPE_MISMATCH,
                           description=f'Shapes: {a.shape} and {b.shape}')
            return self.dot(a, b)
        if isinstance(a, Matrix) and isinstance(b, Scalar):
            return self.for_each_element_do(self.mul, a, b)

        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Multiplication on {type(a)} and {type(b)}')

    def less(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(int(a.value < b.value))
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Test if less on {type(a)} and {type(b)}')

    def greater(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(int(a.value > b.value))
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Test if greater on {type(a)} and {type(b)}')

    def less_or_equal(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(int(a.value <= b.value))
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Test if less or equal on {type(a)} and {type(b)}')

    def greater_or_equal(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(int(a.value >= b.value))
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Test if greater or equal on {type(a)} and {type(b)}')

    def equal(self, a, b):
        if type(a) != type(b):
            self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                       description=f'Test if equal on {type(a)} and {type(b)}')
        return a == b

    def not_equal(self, a, b):
        if type(a) != type(b):
            self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                       description=f'Test if not equal on {type(a)} and {type(b)}')
        return a != b

    def pow(self, a, b):
        if isinstance(a, Scalar) and isinstance(b, Scalar):
            return Scalar(a.value ** b.value)
        if isinstance(a, Matrix) and isinstance(b, Scalar):
            if not b.value.is_integer():
                self.error(error_code=ErrorCode.MATRIX_FLOAT_POW,
                           description=f'The float is {b.value}')
            result = a
            for _ in range(int(b.value)-1):
                result = self.dot(result, a)
        self.error(error_code=ErrorCode.UNSUPPORTED_OPERATION,
                   description=f'Power operation on {type(a)} and {type(b)}')

    def for_each_element_do(self, operation, a, b):
        if isinstance(b, Scalar):
            if not len(a):
                self.error(error_code=ErrorCode.EMPTY_MTRX_OP)
            for row_of_a in a.rows:
                for i in range(a.shape[1]):
                    row_of_a[i] = operation(row_of_a[i], b)
            return a

        # matrix is empty
        if not len(a):
            return a

        rows = []
        for row_of_a, row_of_b in zip(a.rows, b.rows):
            row = MatrixRow([])
            for element_in_row_of_a, element_in_row_of_b\
                    in zip(row_of_a.elements, row_of_b.elements):
                row.append(operation(element_in_row_of_a, element_in_row_of_b))
            rows.append(row)
        return Matrix(rows)

    def dot(self, a, b):
        rows = []
        for i in range(a.shape[0]):
            rows.append(MatrixRow([]))
            for j in range(b.shape[1]):
                rows[i].append(Scalar(0))
                for k in range(b.shape[0]):
                    mul = self.mul(a[i][k], b[k][j])
                    add = self.add(rows[i][j], mul)
                    rows[i][j] = add
        return Matrix(rows)

    def error(self, error_code=None, id='', description=''):
        raise InterpreterError(error_code, id, description)
