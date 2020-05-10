from Error import ParserError, ErrorCode, ErrorDescription
from Lexer.Lexer import Lexer
from Lexer.Token import TokenType
from Objects.Program import Program
from Objects.Function import *
from Objects.Statement import *
from Objects.Identifier import *
from Objects.String import *
from Objects.Matrix import *
from Objects.Scalar import *
from Objects.Operators import *


class Parser:
    def __init__(self, source):
        self.lexer = Lexer(source)
        self.source = source
        self.start_of_object_pos = 0

    def expect(self, expected_token_type):
        if self.lexer.current_token.type != expected_token_type:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN, expected=expected_token_type)
        prev_token = self.lexer.current_token
        self.lexer.build_next_token()
        return prev_token

    def expect_not_none(self, tested_object, error_description=''):
        if tested_object is None:
            self.error(error_code=ErrorCode.EXPECTED_NOT_NONE,
                       description=error_description)
        return tested_object

    def parse_program(self):
        toplevel_objects = []

        while (parsed_object := self.try_to_parse_fun_definition()) or\
                (parsed_object := self.try_to_parse_statement()):
            toplevel_objects.append(parsed_object)
            self.start_of_object_pos = self.lexer.current_token.position.pos

        self.expect(TokenType.ETX)

        return Program(toplevel_objects)

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.build_next_token()

        fun_id = Identifier(self.expect(TokenType.ID))

        self.expect(TokenType.LPAREN)

        parameter_list = self.try_to_parse_fun_parameters()

        self.expect(TokenType.RPAREN)

        statement = self.expect_not_none(
            self.try_to_parse_statement(),
            error_description=ErrorDescription.EMPTY_FUN_BODY
        )

        return FunctionDefinition(fun_id, parameter_list, statement)

    def try_to_parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        parameter_list = [self.expect_parameter()]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            parameter_list.append(self.expect_parameter())

        return parameter_list

    def expect_parameter(self):
        return Identifier(self.expect(TokenType.ID))

    def try_to_parse_statement(self):
        for try_to_parse_statement in [self.try_to_parse_while_loop,
                                       self.try_to_parse_for_loop,
                                       self.try_to_parse_if_statement,
                                       self.try_to_parse_compound_statement]:
            if statement := try_to_parse_statement():
                return statement

        #
        # Handle do_while_loop and (return)expression
        # apart from other statements
        # because of the mandatory semi at the end
        #
        for try_to_parse_before_semi in [self.try_to_parse_do_while_loop,
                                         self.try_to_parse_expression,
                                         self.try_to_parse_ret_statement]:
            if statement := try_to_parse_before_semi():
                self.expect(TokenType.SEMI)
                return statement

        if self.lexer.current_token.type == TokenType.SEMI:
            self.lexer.build_next_token()
            return EmptyStatement()
        return None

    def try_to_parse_do_while_loop(self):
        if self.lexer.current_token.type != TokenType.DO:
            return None
        self.lexer.build_next_token()

        statement = self.expect_not_none(
            self.try_to_parse_statement(),
            error_description=ErrorDescription.EMPTY_DO_WHILE_BODY
        )

        self.expect(TokenType.WHILE)

        self.expect(TokenType.LPAREN)

        condition_expression = self.expect_not_none(
            self.try_to_parse_condition_expression(),
            error_description=ErrorDescription.EMPTY_DO_WHILE_CONDITION
        )

        self.expect(TokenType.RPAREN)

        return DoWhileLoop(statement, condition_expression)

    def try_to_parse_while_loop(self):
        if self.lexer.current_token.type != TokenType.WHILE:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        condition_expression = self.expect_not_none(
            self.try_to_parse_condition_expression(),
            error_description=ErrorDescription.EMPTY_WHILE_CONDITION
        )

        self.expect(TokenType.RPAREN)

        statement = self.expect_not_none(
            self.try_to_parse_statement(),
            error_description=ErrorDescription.EMPTY_WHILE_BODY
        )

        return WhileLoop(statement, condition_expression)

    def try_to_parse_for_loop(self):
        if self.lexer.current_token.type != TokenType.FOR:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        iterator = Identifier(self.expect(TokenType.ID))

        self.expect(TokenType.IN)

        iterable = self.expect_not_none(
            self.try_to_parse_iterable(),
            error_description=ErrorDescription.NO_ITERABLE
        )

        self.expect(TokenType.RPAREN)

        statement = self.expect_not_none(
            self.try_to_parse_statement(),
            error_description=ErrorDescription.EMPTY_FOR_BODY
        )

        return ForLoop(iterator, iterable, statement)

    def try_to_parse_iterable(self):
        for parse_iterable in [self.try_to_parse_id,
                               self.try_to_parse_matrix,
                               self.try_to_parse_string]:
            if (iterable := parse_iterable()) is not None:
                return iterable
        return None

    def try_to_parse_if_statement(self):
        if self.lexer.current_token.type != TokenType.IF:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        condition_expression = self.expect_not_none(
            self.try_to_parse_condition_expression(),
            error_description=ErrorDescription.EMPTY_IF_CONDITION
        )

        self.expect(TokenType.RPAREN)

        statement = self.expect_not_none(
            self.try_to_parse_statement(),
            error_description=ErrorDescription.EMPTY_IF_BODY
        )

        else_statement = None

        if self.lexer.current_token.type == TokenType.ELSE:
            self.lexer.build_next_token()

            else_statement = self.expect_not_none(
                self.try_to_parse_statement(),
                error_description=ErrorDescription.EMPTY_ELSE_BODY
            )

        return IfStatement(condition_expression, statement, else_statement)

    def try_to_parse_compound_statement(self):
        if self.lexer.current_token.type != TokenType.LCURB:
            return None
        self.lexer.build_next_token()

        statement_list = []

        while statement := self.try_to_parse_statement():
            statement_list.append(statement)

        if len(statement_list) == 0:
            self.error(
                ErrorCode.EXPECTED_NOT_NONE,
                description=ErrorDescription.EMPTY_COMPOUND_STATEMENT
            )

        self.expect(TokenType.RCURB)

        return CompoundStatement(statement_list)

    def try_to_parse_ret_statement(self):
        if self.lexer.current_token.type != TokenType.RETURN:
            return None
        self.lexer.build_next_token()

        expression = self.expect_not_none(
            self.try_to_parse_expression(),
            error_description=ErrorDescription.EMPTY_RET_BODY
        )

        return ReturnStatement(expression)

    def try_to_parse_expression(self):
        if (lvalue := self.try_to_parse_condition_expression()) is None:
            return None

        if self.lexer.current_token.type != TokenType.ASSIGN:
            return lvalue
        if not isinstance(lvalue, Identifier):
            self.error(error_code=ErrorCode.ASSIGNTONOTID)

        self.lexer.build_next_token()

        # Allow nested assignments (right connectivity)
        rvalue = self.expect_not_none(
            self.try_to_parse_expression(),
            error_description=ErrorDescription.NO_RVALUE
        )

        return Assignment(lvalue, rvalue)

    def try_to_parse_condition_expression(self):
        lvalue = self.try_to_parse_andExpression()

        while self.lexer.current_token.type == TokenType.OR:
            op = self.lexer.current_token
            self.lexer.build_next_token()

            rvalue = self.expect_not_none(
                self.try_to_parse_andExpression(),
                error_description=ErrorDescription.NO_RVALUE
            )
            lvalue = BinaryOperator(lvalue, op, rvalue)

        return lvalue

    def try_to_parse_andExpression(self):
        lvalue = self.try_to_parse_equality_expression()

        while self.lexer.current_token.type == TokenType.AND:
            op = self.lexer.current_token
            self.lexer.build_next_token()

            rvalue = self.expect_not_none(
                self.try_to_parse_equality_expression(),
                error_description=ErrorDescription.NO_RVALUE
            )
            lvalue = BinaryOperator(lvalue, op, rvalue)

        return lvalue

    def try_to_parse_equality_expression(self):
        lvalue = self.try_to_parse_relative_expression()

        while self.lexer.current_token.type in [TokenType.EQ,
                                                TokenType.NEQ]:
            op = self.lexer.current_token
            self.lexer.build_next_token()

            rvalue = self.expect_not_none(
                self.try_to_parse_relative_expression(),
                error_description=ErrorDescription.NO_RVALUE
            )
            lvalue = BinaryOperator(lvalue, op, rvalue)

        return lvalue

    def try_to_parse_relative_expression(self):
        lvalue = self.try_to_parse_arithmetic_expression()

        while self.lexer.current_token.type in [TokenType.LEQ,
                                                TokenType.LESS,
                                                TokenType.GEQ,
                                                TokenType.GRE]:
            op = self.lexer.current_token
            self.lexer.build_next_token()

            rvalue = self.expect_not_none(
                self.try_to_parse_arithmetic_expression(),
                error_description=ErrorDescription.NO_RVALUE
            )
            lvalue = BinaryOperator(lvalue, op, rvalue)

        return lvalue

    def try_to_parse_arithmetic_expression(self):
        lvalue = self.try_to_parse_term()

        while self.lexer.current_token.type in [TokenType.PLUS,
                                                TokenType.MINUS]:
            op = self.lexer.current_token
            self.lexer.build_next_token()

            rvalue = self.expect_not_none(
                self.try_to_parse_term(),
                error_description=ErrorDescription.NO_RVALUE
            )
            lvalue = BinaryOperator(lvalue, op, rvalue)

        return lvalue

    def try_to_parse_term(self):
        lvalue = self.try_to_parse_miniterm()

        while self.lexer.current_token.type in [TokenType.MUL,
                                                TokenType.FLOAT_DIV,
                                                TokenType.INTEGER_DIV,
                                                TokenType.MODULO]:
            op = self.lexer.current_token
            self.lexer.build_next_token()

            rvalue = self.expect_not_none(
                self.try_to_parse_miniterm(),
                error_description=ErrorDescription.NO_RVALUE
            )
            lvalue = BinaryOperator(lvalue, op, rvalue)

        return lvalue

    def try_to_parse_miniterm(self):
        if self.lexer.current_token.type not in [TokenType.PLUS,
                                                 TokenType.MINUS,
                                                 TokenType.NOT]:
            return self.try_to_parse_microterm()

        op = self.lexer.current_token
        self.lexer.build_next_token()

        # Allow nested unary operators
        rvalue = self.expect_not_none(
            self.try_to_parse_miniterm(),
            error_description=ErrorDescription.NO_RVALUE
        )
        return UnaryOperator(op, rvalue)

    def try_to_parse_microterm(self):
        lvalue = self.try_to_parse_factor()

        if self.lexer.current_token.type != TokenType.POW:
            return lvalue
        op = self.lexer.current_token
        self.lexer.build_next_token()

        # Do not allow nested power operations
        rvalue = self.expect_not_none(
            self.try_to_parse_factor(),
            error_description=ErrorDescription.NO_RVALUE
        )
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_factor(self):
        for try_to_parse_factor in [self.try_to_parse_constant,
                                    self.try_to_parse_non_constant,
                                    self.try_to_parse_expression_inside_parentheses]:
            if (factor := try_to_parse_factor()) is not None:
                return factor
        return None

    def try_to_parse_constant(self):
        for try_to_parse_constant in [self.try_to_parse_scalar,
                                      self.try_to_parse_matrix]:
            if (constant := try_to_parse_constant()) is not None:
                return constant
        return None

    def try_to_parse_non_constant(self):
        if (id := self.try_to_parse_id()) is None:
            return None

        for parse_method in [self.try_to_parse_function_call,
                             self.try_to_parse_matrix_subscripting]:
            if (non_constant := parse_method(id)) is not None:
                return non_constant
        return id

    def try_to_parse_expression_inside_parentheses(self):
        if self.lexer.current_token.type != TokenType.LPAREN:
            return None
        self.lexer.build_next_token()

        # allow parentheses to have no expression inside
        # do not check if expression is None
        expression = self.try_to_parse_expression()
        self.expect(TokenType.RPAREN)
        return expression

    def try_to_parse_scalar(self):
        if self.lexer.current_token.type != TokenType.SCALAR:
            return None
        scalar = Scalar(self.lexer.current_token)
        self.lexer.build_next_token()

        return scalar

    def try_to_parse_matrix(self):
        if self.lexer.current_token.type != TokenType.LBRACK:
            return None
        self.lexer.build_next_token()

        rows = self.try_to_parse_matrix_rows()

        self.expect(TokenType.RBRACK)
        return Matrix(rows)

    def try_to_parse_matrix_rows(self):
        if (row := self.try_to_parse_row()) is None:
            return []
        rows = [row]

        while self.lexer.current_token.type == TokenType.SEMI:
            self.lexer.build_next_token()

            matrix_row = self.expect_not_none(
                self.try_to_parse_row(),
                error_description=ErrorDescription.EMPTY_MTRX_ROW
            )

            rows.append(matrix_row)
            if len(rows[-1]) != len(rows[-2]):
                self.error(
                    error_code=ErrorCode.MTRX_ROW_LEN_MISMATCH,
                    description='Rows in matrix should have same length.'
                )
        return rows

    def try_to_parse_row(self):
        if (expression := self.try_to_parse_condition_expression()) is None:
            return None
        expressions = [expression]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            expression = self.expect_not_none(
                self.try_to_parse_condition_expression(),
                error_description=ErrorDescription.NO_ITEM
            )

            expressions.append(expression)

        return MatrixRow(expressions)

    def try_to_parse_id(self):
        if self.lexer.current_token.type != TokenType.ID:
            return None
        token_id = self.lexer.current_token
        self.lexer.build_next_token()

        return Identifier(token_id)

    def try_to_parse_function_call(self, id):
        if self.lexer.current_token.type != TokenType.LPAREN:
            return None
        self.lexer.build_next_token()

        argument_list = self.try_to_parse_function_arguments()

        self.expect(TokenType.RPAREN)

        return FunctionCall(id, argument_list)

    def try_to_parse_function_arguments(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        if (expression := self.try_to_parse_expression()) is None:
            return []
        argument_list = [expression]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            expression = self.expect_not_none(
                self.try_to_parse_expression(),
                error_description=ErrorDescription.NO_ARGUMENT
            )
            argument_list.append(expression)

        return argument_list

    def try_to_parse_matrix_subscripting(self, id):
        if self.lexer.current_token.type != TokenType.LBRACK:
            return None
        self.lexer.build_next_token()

        idx = self.try_to_parse_index()

        idx2 = None
        if self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            idx2 = self.try_to_parse_index()

        self.expect(TokenType.RBRACK)
        return MatrixSubscripting(id, idx, idx2)

    def try_to_parse_index(self):
        if self.lexer.current_token.type == TokenType.COLON:
            self.lexer.build_next_token()

            return MatrixIndex(None, True)

        expression = self.expect_not_none(
            self.try_to_parse_expression(),
            error_description=ErrorDescription.NO_INDEX
        )
        return MatrixIndex(expression)

    def try_to_parse_string(self):
        if self.lexer.current_token.type != TokenType.STRING:
            return None
        token_string = self.lexer.current_token
        self.lexer.build_next_token()

        return String(token_string)

    def error(self, error_code=None, expected=None, description=''):
        raise ParserError(
            error_code=error_code,
            current_token=self.lexer.current_token,
            source_pos=self.start_of_object_pos,
            source=self.source,
            description=description,
            expected_token_type=expected
        )
