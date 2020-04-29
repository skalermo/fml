from Error import ParserError, ErrorCode
from Source.Position import Position
from Lexer.Token import TokenType
from Parser.Objects.Program import Program
from Parser.Objects.Function import *
from Parser.Objects.Statement import *
from Parser.Objects.Identifier import *
from Parser.Objects.String import *
from Parser.Objects.Matrix import *
from Parser.Objects.Scalar import *
from Parser.Objects.Operators import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # self.program = self.parse_program()

    def expect(self, expected_token_type):
        if self.lexer.current_token.type != expected_token_type:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN, expected=expected_token_type)
        prev_token = self.lexer.current_token
        self.lexer.build_next_token()
        return prev_token

    def parse_program(self):
        toplevel_objects = []

        while (parsed_object := self.try_to_parse_fun_definition()) or\
                (parsed_object := self.try_to_parse_statement()):
            toplevel_objects.append(parsed_object)

        return Program(toplevel_objects)

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.source.update_context_start(self.lexer.current_token.position.pos)
        self.lexer.build_next_token()

        fun_id = self.expect(TokenType.ID)

        self.expect(TokenType.LPAREN)

        parameter_list = self.try_to_parse_fun_parameters()

        self.expect(TokenType.RPAREN)

        if (statement := self.try_to_parse_statement()) is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        return FunctionDefinition(fun_id, parameter_list, statement)

    def try_to_parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        parameter_list = [self.expect(TokenType.ID)]

        while self.lexer.current_token.type != TokenType.RPAREN:
            self.expect(TokenType.COMMA)

            parameter_list.append(self.expect(TokenType.ID))

        return parameter_list

    def try_to_parse_statement(self):
        self.lexer.source.update_context_start(self.lexer.current_token.position.pos)

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

        if (statement := self.try_to_parse_statement()) is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        self.expect(TokenType.WHILE)

        self.expect(TokenType.LPAREN)

        condition_expression = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        return DoWhileLoop(statement, condition_expression)

    def try_to_parse_while_loop(self):
        if self.lexer.current_token.type != TokenType.WHILE:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        if (condition_expression := self.try_to_parse_condition_expression()) is None:
            self.error(error_code=ErrorCode.EMPTY_COND)

        self.expect(TokenType.RPAREN)

        if (statement := self.try_to_parse_statement()) is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        return WhileLoop(statement, condition_expression)

    def try_to_parse_for_loop(self):
        if self.lexer.current_token.type != TokenType.FOR:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        token_iterator = self.expect(TokenType.ID)

        self.expect(TokenType.IN)

        if (iterable := self.try_to_parse_iterable()) is None:
            self.error(error_code=ErrorCode.EXPECTED_ITERABLE)

        self.expect(TokenType.RPAREN)

        statement = self.try_to_parse_statement()
        return ForLoop(token_iterator, iterable, statement)

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

        if (condition_expression := self.try_to_parse_condition_expression()) is None:
            self.error(error_code=ErrorCode.EMPTY_COND)

        self.expect(TokenType.RPAREN)

        if (statement := self.try_to_parse_statement()) is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        else_statement = None

        if self.lexer.current_token.type == TokenType.ELSE:
            self.lexer.build_next_token()

            if (else_statement := self.try_to_parse_statement()) is None:
                self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        return IfStatement(condition_expression, statement, else_statement)

    def try_to_parse_compound_statement(self):
        if self.lexer.current_token.type != TokenType.LCURB:
            return None
        self.lexer.build_next_token()

        statement_list = []

        while statement := self.try_to_parse_statement():
            statement_list.append(statement)

        if len(statement_list) == 0:
            self.error(ErrorCode.EXPECTED_STATEMENT)

        self.expect(TokenType.RCURB)

        return CompoundStatement(statement_list)

    def try_to_parse_ret_statement(self):
        if self.lexer.current_token.type != TokenType.RETURN:
            return None
        self.lexer.build_next_token()

        if (expression := self.try_to_parse_expression()) is None:
            self.error(error_code=ErrorCode.EXPECTED_EXPRESSION)

        return ReturnStatement(expression)

    def try_to_parse_expression(self):
        lvalue = self.try_to_parse_condition_expression()

        if self.lexer.current_token.type != TokenType.ASSIGN:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        # Here parsing expression - allows nested assignments
        if (rvalue := self.try_to_parse_expression()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_condition_expression(self):
        lvalue = self.try_to_parse_andExpression()

        if self.lexer.current_token.type != TokenType.OR:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_condition_expression()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_andExpression(self):
        lvalue = self.try_to_parse_equality_expression()

        if self.lexer.current_token.type != TokenType.AND:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_andExpression()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_equality_expression(self):
        lvalue = self.try_to_parse_relative_expression()

        if self.lexer.current_token.type not in [TokenType.EQ,
                                                 TokenType.NEQ]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_equality_expression()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_relative_expression(self):
        lvalue = self.try_to_parse_arithmetic_expression()

        if self.lexer.current_token.type not in [TokenType.LEQ,
                                                 TokenType.LESS,
                                                 TokenType.GEQ,
                                                 TokenType.GRE]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_relative_expression()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_arithmetic_expression(self):
        lvalue = self.try_to_parse_term()

        if self.lexer.current_token.type not in [TokenType.PLUS,
                                                 TokenType.MINUS]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_arithmetic_expression()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_term(self):
        lvalue = self.try_to_parse_miniterm()

        if self.lexer.current_token.type not in [TokenType.MUL,
                                                 TokenType.FLOAT_DIV,
                                                 TokenType.INTEGER_DIV,
                                                 TokenType.MODULO]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_term()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_miniterm(self):
        if self.lexer.current_token.type not in [TokenType.PLUS,
                                                 TokenType.MINUS,
                                                 TokenType.NOT]:
            return self.try_to_parse_microterm()

        op = self.lexer.current_token
        return UnaryOperator(op, self.try_to_parse_microterm())

    def try_to_parse_microterm(self):
        lvalue = self.try_to_parse_factor()

        if self.lexer.current_token.type != TokenType.POW:
            return lvalue
        op = self.lexer.current_token
        self.lexer.build_next_token()

        if (rvalue := self.try_to_parse_factor()) is None:
            self.error(error_code=ErrorCode.RVAL_FAIL)
        return BinaryOperator(lvalue, op, rvalue)

    def try_to_parse_factor(self):
        for try_to_parse_factor in [self.try_to_parse_constant,
                                    self.try_to_parse_non_constant,
                                    self.try_to_parse_expression_in_brackets]:
            if factor := try_to_parse_factor():
                return factor
        return None

    def try_to_parse_constant(self):
        for try_to_parse_constant in [self.try_to_parse_scalar,
                                      self.try_to_parse_matrix]:
            if constant := try_to_parse_constant():
                return constant
        return None

    def try_to_parse_non_constant(self):
        if (id := self.try_to_parse_id()) is None:
            return None

        for parse_method in [self.try_to_parse_function_call,
                             self.try_to_parse_matrix_subscripting]:
            if non_constant := parse_method(id):
                return non_constant
        return id

    def try_to_parse_expression_in_brackets(self):
        if self.lexer.current_token.type != TokenType.LPAREN:
            return None
        self.lexer.build_next_token()

        # maybe be brackets with no expression
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

        rows = [self.try_to_parse_matrix_row()]

        while self.lexer.current_token.type == TokenType.SEMI:
            self.lexer.build_next_token()

            if (matrix_row := self.try_to_parse_matrix_row()) is None:
                self.error(error_code=ErrorCode.EXPECTED_MTRX_ROW)

            rows.append(matrix_row)
            if len(rows[-1]) != len(rows[-2]):
                self.error(error_code=ErrorCode.MTRX_ROW_LEN_MISMATCH)

        self.expect(TokenType.RBRACK)

        return Matrix(rows)

    def try_to_parse_id(self):
        if self.lexer.current_token.type != TokenType.ID:
            return None
        token_id = self.lexer.current_token
        self.lexer.build_next_token()

        return Identifier(token_id)

    def try_to_parse_function_call(self, token_id):
        if self.lexer.current_token.type != TokenType.LPAREN:
            return None
        self.lexer.build_next_token()

        argument_list = [self.try_to_parse_expression()]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            argument_list.append(self.try_to_parse_expression())

        self.expect(TokenType.RPAREN)

        return FunctionCall(token_id, argument_list)

    def try_to_parse_matrix_subscripting(self, token_id):
        if self.lexer.current_token.type != TokenType.LBRACK:
            return None
        self.lexer.build_next_token()

        idx = self.try_to_parse_index()

        idx2 = None
        if self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            idx2 = self.try_to_parse_index()

        self.expect(TokenType.RBRACK)
        return MatrixSubscripting(token_id, idx, idx2)

    def try_to_parse_index(self):
        if self.lexer.current_token.type == TokenType.COLON:
            self.lexer.build_next_token()

            return MatrixIndex(None, True)

        if (expression := self.try_to_parse_expression()) is None:
            self.error(error_code=ErrorCode.EXPECTED_EXPRESSION)
        return MatrixIndex(expression)

    def try_to_parse_string(self):
        if self.lexer.current_token.type != TokenType.STRING:
            return None
        token_string = self.lexer.current_token
        self.lexer.build_next_token()

        return String(token_string)

    def try_to_parse_matrix_row(self):
        if (expression := self.try_to_parse_condition_expression()) is None:
            return None
        expressions = [expression]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()

            if (expression := self.try_to_parse_condition_expression()) is None:
                self.error(error_code=ErrorCode.EXPECTED_MTRX_ITEM)

            expressions.append(expression)

        return MatrixRow(expressions)

    def error(self, error_code=None, expected=None):
        raise ParserError(
            error_code=error_code,
            position=self.lexer.current_token.position,
            context=self.lexer.source.get_last_context(),
            source_type=self.lexer.source.get_source_type(),
            expected_token_type=expected
        )
