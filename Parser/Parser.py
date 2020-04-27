from Error import ParserError, ErrorCode
from Source.Position import Position
from Lexer.Token import TokenType
from Parser.Objects.Program import Program
from Parser.Objects.Function import *
from Parser.Objects.Statement import *
from Parser.Objects.Expression import *
from Parser.Objects.Identifier import *
from Parser.Objects.String import *
from Parser.Objects.Matrix import *
from Parser.Objects.Scalar import *
from Parser.Objects.Operators import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.program = self.parse_program()

    def expect(self, expected_token_type):
        if self.lexer.current_token.type != expected_token_type:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
        self.lexer.build_next_token()

    def parse_program(self):
        toplevel_objects = []

        while (parsed_object := self.try_to_parse_fun_definition()) or\
                (parsed_object := self.try_to_parse_statement()):
            toplevel_objects.append(parsed_object)

        return Program(toplevel_objects)

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.source.update_context_start()

        self.lexer.build_next_token()

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        fun_id = self.lexer.current_token.value
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        parameter_list = self.try_to_parse_fun_parameters()

        self.expect(TokenType.RPAREN)

        if statement := self.try_to_parse_statement() is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        return FunctionDefinition(fun_id, parameter_list, statement)

    def try_to_parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        parameter_list = [self.lexer.current_token.value]
        self.lexer.build_next_token()

        while self.lexer.current_token.type != TokenType.RPAREN:
            if self.lexer.current_token.type != TokenType.COMMA:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            self.lexer.build_next_token()

            if self.lexer.current_token.type != TokenType.ID:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            parameter_list.append(self.lexer.current_token)
            self.lexer.build_next_token()

        return parameter_list

    def try_to_parse_statement(self):
        self.lexer.source.update_context_start()
        #
        # Handle do_while_loop and (return)expression
        # apart from other statements
        # because of the mandatory semi at the end
        #
        for try_to_parse_before_semi in [self.try_to_parse_do_while_loop,
                                         self.try_to_parse_ret_statement,
                                         self.try_to_parse_expression]:
            if statement := try_to_parse_before_semi():
                self.expect(TokenType.SEMI)
                return statement

        for try_to_parse_statement in [self.try_to_parse_while_loop,
                                       self.try_to_parse_for_loop,
                                       self.try_to_parse_if_statement,
                                       self.try_to_parse_compound_statement,
                                       self.try_to_parse_ret_statement]:
            if statement := try_to_parse_statement():
                return statement
        return None

    def try_to_parse_do_while_loop(self):
        if self.lexer.current_token.type != TokenType.DO:
            return None
        self.lexer.build_next_token()

        statement = self.try_to_parse_statement()

        self.expect(TokenType.WHILE)

        self.expect(TokenType.LPAREN)

        condition_expression = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        return DoWhileLoop(statement, condition_expression)

    def try_to_parse_while_loop(self):
        if self.lexer.current_token.type != TokenType.WHILE:
            return None

        self.expect(TokenType.LPAREN)

        condition_expression = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        statement = self.try_to_parse_statement()
        return WhileLoop(statement, condition_expression)

    def try_to_parse_for_loop(self):
        if self.lexer.current_token.type != TokenType.FOR:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        # todo decide which to pass to variables: str or token
        var = self.lexer.current_token.value
        self.lexer.build_next_token()
        self.expect(TokenType.IN)

        for parse_iterable in [self.try_to_parse_id,
                               self.try_to_parse_matrix,
                               self.try_to_parse_string]:
            iterable = parse_iterable()
        self.expect(TokenType.RPAREN)
        statement = self.try_to_parse_statement()
        return ForLoop(var, iterable, statement)

    def try_to_parse_if_statement(self):
        if self.lexer.current_token.type != TokenType.IF:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        condition_expression = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        statement = self.try_to_parse_statement()
        else_statement = None

        if self.lexer.current_token.type == TokenType.ELSE:
            self.lexer.build_next_token()
            else_statement = self.try_to_parse_statement()

        return IfStatement(condition_expression, statement, else_statement)

    def try_to_parse_compound_statement(self):
        if self.lexer.current_token != TokenType.LCURB:
            return None
        self.lexer.build_next_token()

        statement_list = []

        while statement := self.try_to_parse_statement():
            statement_list.append(statement)

        self.expect(TokenType.RCURB)

        return CompoundStatement(statement_list)

    def try_to_parse_ret_statement(self):
        if self.lexer.current_token.type != TokenType.RETURN:
            return None
        self.lexer.build_next_token()

        expression = self.try_to_parse_expression()

        return ReturnStatement(expression)

    def try_to_parse_expression(self):
        #
        # It could be either of these:
        #   id = expression;
        #   expression;
        #
        if lvalue := self.try_to_parse_id() is None:
            return self.try_to_parse_condition_expression()

        if self.lexer.current_token.type != TokenType.ASSIGN:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_expression())

    def try_to_parse_condition_expression(self):
        lvalue = self.try_to_parse_andExpression()

        if self.lexer.current_token.type != TokenType.OR:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_condition_expression())

    def try_to_parse_andExpression(self):
        lvalue = self.try_to_parse_equality_expression()

        if self.lexer.current_token.type != TokenType.AND:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_condition_expression())

    def try_to_parse_equality_expression(self):
        lvalue = self.try_to_parse_relative_expression()

        if self.lexer.current_token.type not in [TokenType.EQ,
                                            TokenType.NEQ]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_equality_expression())

    def try_to_parse_relative_expression(self):
        lvalue = self.try_to_parse_arithmetic_expression()

        if self.lexer.current_token.type not in [TokenType.LEQ,
                                                 TokenType.LESS,
                                                 TokenType.GEQ,
                                                 TokenType.GRE]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_relative_expression())

    def try_to_parse_arithmetic_expression(self):
        lvalue = self.try_to_parse_term()

        if self.lexer.current_token.type not in [TokenType.PLUS,
                                                 TokenType.MINUS]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_arithmetic_expression())

    def try_to_parse_term(self):
        lvalue = self.try_to_parse_miniterm()

        if self.lexer.current_token.type not in [TokenType.MUL,
                                                 TokenType.FLOAT_DIV,
                                                 TokenType.INTEGER_DIV,
                                                 TokenType.MODULO]:
            return lvalue

        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_term())

    def try_to_parse_miniterm(self):
        op = TokenType.PLUS
        if self.lexer.current_token.type in [TokenType.PLUS,
                                             TokenType.MINUS,
                                             TokenType.NOT]:
            op = self.lexer.current_token
        return UnaryOperator(op, self.try_to_parse_microterm())

    def try_to_parse_microterm(self):
        lvalue = self.try_to_parse_factor()

        if self.lexer.current_token.type != TokenType.POW:
            return lvalue
        op = self.lexer.current_token
        self.lexer.build_next_token()

        return BinaryOperator(lvalue, op, self.try_to_parse_factor())

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
        if id := self.try_to_parse_id() is None:
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
        expression = self.try_to_parse_expression()
        self.expect(TokenType.RPAREN)
        return expression

    def try_to_parse_scalar(self):
        if self.lexer.current_token.type != TokenType.SCALAR:
            return None
        scalar = Scalar(self.lexer.current_token())
        self.lexer.build_next_token()
        return scalar

    def try_to_parse_matrix(self):
        if self.lexer.current_token.type != TokenType.LBRACK:
            return None
        self.lexer.build_next_token()

        rows = [self.try_to_parse_matrix_row()]

        while self.lexer.current_token.type == TokenType.SEMI:
            self.lexer.build_next_token()
            rows.append(self.try_to_parse_matrix_row())
            if len(rows[-1]) != len(rows[-2]):
                self.error(error_code=ErrorCode.MTRX_ROW_LEN_MISMATCH)

        return Matrix(rows)

    def try_to_parse_id(self):
        if self.lexer.current_token.type != TokenType.ID:
            return None
        id = self.lexer.current_token.value
        self.lexer.build_next_token()
        return Identifier(id)

    def try_to_parse_function_call(self, id):
        if self.lexer.current_token.type != TokenType.LPAREN:
            return None
        self.lexer.build_next_token()
        argument_list = [self.try_to_parse_expression()]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()
            argument_list.append(self.try_to_parse_expression())

        return FunctionCall(id, argument_list)

    def try_to_parse_matrix_subscripting(self, id):
        if self.lexer.current_token.type != TokenType.LBRACK:
            return None
        self.lexer.build_next_token()
        idx = self.try_to_parse_index()
        idx2 = None
        if self.lexer.current_token == TokenType.COMMA:
            self.lexer.build_next_token()
            idx2 = self.try_to_parse_index()
        return MatrixSubscripting(id, idx, idx2)

    def try_to_parse_index(self):
        if self.lexer.current_token.type == TokenType.COLON:
            self.lexer.build_next_token()
            return MatrixIndex(None, True)
        return MatrixIndex(self.try_to_parse_expression())

    def try_to_parse_string(self):
        if self.lexer.current_token.type != TokenType.STRING:
            return None
        return String(self.lexer.current_token)

    def try_to_parse_matrix_row(self):
        expressions = [self.try_to_parse_expression()]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()
            expressions.append(self.try_to_parse_expression())

        return MatrixRow(expressions)

    def error(self, error_code=None):
        s = 'line: {position.line} column: {position.column}'.format(
            position=Position(self.lexer.source)
        )
        raise ParserError(
            error_code=error_code,
            message=s,
            token=self.lexer.current_token,
            context=self.lexer.source.get_last_context()
        )

    # def try_to_parse_assignment(self, id):
    #     if self.lexer.current_token.type != TokenType.EQ:
    #         return None
    #     self.lexer.build_next_token()
    #
    #     lhs = Identifier(id.value)
    #
    #     for try_to_parse_assignment in [self.try_to_parse_string,
    #                                     self.try_to_parse_condition_expression]:
    #         if rhs := try_to_parse_assignment():
    #             return Assignment(lhs, rhs)
    #     return None