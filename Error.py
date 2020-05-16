import sys


# Custom exception handler.
# Works in terminal.
def handler(exception_type, exception, traceback):
    print(exception.message)
sys.excepthook = handler


class ErrorCode:
    TOKEN_BUILD_FAIL = 'Failed to build a token'
    EXCEED_MAX_ID_SIZE = 'Exceeded max length of an identifier'

    UNEXPECTED_TOKEN = 'Unexpected token'
    EXPECTED_NOT_NONE = 'No object parsed.'

    MTRX_ROW_LEN_MISMATCH = 'Matrix should have rows of the same length'
    ASSIGN_TO_NOT_ID = 'Cannot assign to non-identifier'

    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'
    UNSUPPORTED_BINARY_OPERATION = 'Operation for these types not supported'
    MATRIX_SHAPE_MISMATCH = 'Shapes of matrices do not match'
    ZERO_DIVISION = 'Division or modulo by zero'
    EMPTY_MTRX_OP = 'Cannot perform operation on empty matrix'
    MATRIX_DOT_SHAPE_MISMATCH = 'Cannot perform dot product for matrices'
    MATRIX_FLOAT_POW = 'Cannot perform matrix to the float power operation'
    FLOAT_IDX = 'Matrix index cannot be float'
    OUT_OF_RANGE = 'Matrix index out of range'
    ROW_INDEX_OUT_OF_RANGE = 'Row index out of range'
    COLUMN_INDEX_OUT_OF_RANGE = 'Column index out of range'
    UNSUPPORTED_UNARY_OPERATION = 'Operation for this type not supported'
    FUN_NOT_DEFINED = 'Called function is not defined'
    NUMBER_OF_PARAMS_MISMATCH = 'Wrong number of parameters'
    MAX_RECURSION_DEPTH_EXCEED = 'Maximum recursion depth exceeded'
    SCALAR_LEN = 'Object of type Scalar has no len()'
    UNSUPPORTED_TYPE_ABS = 'Encountered unsupported type of argument in abs()'
    UNSUPPORTED_TYPES_MAX = 'Encountered unsupported types of arguments in max()'
    UNSUPPORTED_TYPES_MIN = 'Encountered unsupported types of arguments in min()'
    UNSUPPORTED_TYPE_ROUND = 'Encountered unsupported type of argument in round()'
    UNSUPPORTED_TYPE_SHAPE = 'Encountered unsupported type of argument in shape()'
    UNSUPPORTED_TYPE_TRANSPOSE = 'Encountered unsupported type of argument in transp()'
    NOT_ITERABLE = 'Object is not iterable'


class ErrorDescription:
    EMPTY_FUN_BODY = 'Function body should not be empty.'
    EMPTY_DO_WHILE_BODY = 'Body of do while loop should not be emtpy.'
    EMPTY_DO_WHILE_CONDITION = 'Condition of do while loop should not be empty.'
    EMPTY_WHILE_BODY = 'Body of while loop should not be empty.'
    EMPTY_WHILE_CONDITION = 'Condition of while loop should not be empty.'
    NO_ITERABLE = 'No iterable found.'
    EMPTY_FOR_BODY = 'Body of for loop should not be empty.'
    EMPTY_IF_CONDITION = 'Condition of if statement should not be empty.'
    EMPTY_IF_BODY = 'Body of if statement should not be empty.'
    EMPTY_ELSE_BODY = 'Body of else statement should not be empty.'
    EMPTY_RET_BODY = 'Expression to return should not be empty.'
    NO_RVALUE = 'Expected rvalue.'
    EMPTY_MTRX_ROW = 'Expected matrix row.'
    NO_ARGUMENT = 'No argument found.'
    NO_INDEX = 'No index found.'
    NO_ITEM = 'No matrix item found.'
    EMPTY_COMPOUND_STATEMENT = 'Compound statement should not be empty.'


class Error(Exception):
    def __init__(self, message):
        self.message = message

        # hide traceback of pycharm
        sys.tracebacklimit = 0

        super().__init__(self.message)


class LexerError(Error):
    def __init__(
            self,
            error_code,
            current_token,
            source
    ):

        self.error_code = error_code
        self.message = ''

        source_type = source.get_source_type()
        error_source = 'File "{source_type}", line {line}, column {column}\n'.format(
            source_type=source_type,
            line=source.line,
            column=source.column
        )

        if current_token is not None:
            source.update_context_start(current_token.position.pos)
        context = source.get_last_context()
        context += source.current_char
        length = min(len(context), source.column)
        context += '\n'

        pointer_line = ''.join([' '*(length-1), '^\n'])
        message = f'{type(self).__name__}: {error_code}\n'

        self.message = ''.join([error_source, context, pointer_line, message])
        super().__init__(self.message)


class ParserError(Error):
    def __init__(self,
                 error_code,
                 current_token,
                 source_pos,
                 source,
                 description,
                 expected_token_type):

        self.expected_token_type = expected_token_type
        self.error_code = error_code
        self.description = description
        self.message = ''

        source_type = source.get_source_type()
        error_source = 'File "{source_type}", line {line}, column {column}\n'.format(
            source_type=source_type,
            line=current_token.position.line,
            column=current_token.position.column
        )

        source.update_context_start(source_pos)
        context = source.get_last_context()
        if not context:
            context = current_token.value

        length = min(len(context), current_token.position.column)
        context += '\n'

        pointer_line = ''.join([' '*(length-1), '^\n'])

        expected = ''
        if error_code == ErrorCode.UNEXPECTED_TOKEN and expected_token_type is not None:
            expected = f', expected {expected_token_type}'
        message = f'{type(self).__name__}: {error_code}{expected}\n'

        if description:
            description += '\n'

        self.message = ''.join([error_source, context, pointer_line, message, description])
        super().__init__(self.message)


class InterpreterError(Error):
    def __init__(self, error_code, id, description):
        self.error_code = error_code
        self.id = id
        self.description = description

        if id:
            id = ''.join(['"', id, '"'])
        message = f'{type(self).__name__}: {error_code} {id}\n'
        if description:
            description += '\n'

        self.message = ''.join([message, description])

        super().__init__(self.message)
