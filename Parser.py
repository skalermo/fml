from Error import ParserError, ErrorCode
from Position import Position
from Token import TokenType
from grammatical_objects.Program import Program
from grammatical_objects.Function import FunctionDefinition
from grammatical_objects.Statement import *
from grammatical_objects.Expression import *
from grammatical_objects.Constants import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.program = self.parse_program()

    def expect(self, expected_token_type):
        if self.lexer.current_token.type != expected_token_type:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
        self.lexer.build_next_token()

    def parse_program(self):
        objects = []
        while (parsed_object := self.try_to_parse_fun_definition()) or\
                (parsed_object := self.try_to_parse_statement()):
            objects.append(parsed_object)

        return Program(objects)

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

        if statement := self.try_to_parse_statement() is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        return FunctionDefinition(fun_id, parameter_list, statement)

    def try_to_parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            self.lexer.build_next_token()
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

        # skip RPAREN
        self.lexer.build_next_token()
        return parameter_list

    def try_to_parse_statement(self):
        # Handle do_while_loop apart from other statements
        # because of the mandatory semi at the end
        self.lexer.source.update_context_start()
        if (statement := self.try_to_parse_do_while_loop()) or \
                (statement := self.try_to_parse_expression()):
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

        logical_expr = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        return DoWhileLoop(statement, logical_expr)

    def try_to_parse_while_loop(self):
        if self.lexer.current_token.type != TokenType.WHILE:
            return None

        self.expect(TokenType.LPAREN)

        logical_expr = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        statement = self.try_to_parse_statement()
        return WhileLoop(statement, logical_expr)

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

        cond_expr = self.try_to_parse_condition_expression()

        self.expect(TokenType.RPAREN)

        statement = self.try_to_parse_statement()
        else_statement = None

        if self.lexer.current_token.type == TokenType.ELSE:
            self.lexer.build_next_token()
            else_statement = self.try_to_parse_statement()

        return IfStatement(cond_expr, statement, else_statement)

    def try_to_parse_compound_statement(self):
        if self.lexer.current_token != TokenType.LCURB:
            return None

        self.lexer.build_next_token()
        statement_list = []
        while self.lexer.current_token != TokenType.RCURB:
            if self.lexer.current_token == TokenType.ETX:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            if statement := self.try_to_parse_statement():
                statement_list.append(statement)

        self.lexer.build_next_token()
        return CompoundStatement(statement_list)

    def try_to_parse_ret_statement(self):
        if self.lexer.current_token.type != TokenType.RETURN:
            return None

        self.lexer.source.update_context_start()

        self.lexer.build_next_token()

        expression = self.try_to_parse_expression()

        self.expect(TokenType.SEMI)
        return ReturnStatement(expression)

    def try_to_parse_expression(self):
        if self.lexer.current_token.type != TokenType.ID:
            return self.try_to_parse_condition_expression()

        id = self.lexer.current_token
        self.lexer.build_next_token()

        for try_to_parse_expression in [self.try_to_parse_assignment,
                                        self.try_to_parse_condition_expression]:
            if expression := try_to_parse_expression(id):
                return expression
        return None

    def try_to_parse_assignment(self, id):
        if self.lexer.current_token.type != TokenType.EQ:
            return None
        self.lexer.build_next_token()

        lhs = Identifier(id.value)

        for try_to_parse_assignment in [self.try_to_parse_string,
                                        self.try_to_parse_condition_expression]:
            if rhs := try_to_parse_assignment():
                return Assignment(lhs, rhs)
        return None

    def try_to_parse_condition_expression(self, first_term=None):
        if first_term is not None:
            a_expr = Identifier(first_term)
        elif a_expr := self.try_to_parse_andExpression() is None:
            return None

        and_expressions = [a_expr]

        while self.lexer.current_token.type == TokenType.OR:
            self.lexer.build_next_token()
            and_expressions.append(self.try_to_parse_andExpression())

        return ConditionExpression(and_expressions)

    def try_to_parse_andExpression(self):
        if e_expr := self.try_to_parse_equality_expression() is None:
            return None

        equality_expressions = [e_expr]

        while self.lexer.current_token.type == TokenType.AND:
            self.lexer.build_next_token()
            equality_expressions.append(self.try_to_parse_equality_expression())

        return AndExpression(equality_expressions)

    def try_to_parse_equality_expression(self):
        if r_expr := self.try_to_parse_relative_expression() is None:
            return None

        relative_expressions = [r_expr]
        operators = []

        while self.lexer.current_token.type in [TokenType.EQ,
                                                TokenType.NEQ]:
            operators.append(self.lexer.current_token.type)
            self.lexer.build_next_token()
            relative_expressions.append(self.try_to_parse_relative_expression())

        return EqualityExpression(relative_expressions, operators)

    def try_to_parse_relative_expression(self):
        if a_expr := self.try_to_parse_arithmetic_expression() is None:
            return None

        arithmetic_expressions = [a_expr]
        operators = []

        while self.lexer.current_token.type in [TokenType.LEQ,
                                                TokenType.LESS,
                                                TokenType.GEQ,
                                                TokenType.GRE]:
            operators.append(self.lexer.current_token.type)
            self.lexer.build_next_token()
            arithmetic_expressions.append(self.try_to_parse_arithmetic_expression())

        return RelativeExpression(arithmetic_expressions, operators)

    def try_to_parse_arithmetic_expression(self):
        if term := self.try_to_parse_term() is None:
            return None

        terms = [term]
        operators = []

        while self.lexer.current_token.type in [TokenType.PLUS,
                                                TokenType.MINUS]:
            operators.append(self.lexer.current_token.type)
            self.lexer.build_next_token()
            terms.append(self.try_to_parse_term())

        return ArithmeticExpression(terms, operators)

    def try_to_parse_term(self):
        if miniterm := self.try_to_parse_miniterm() is None:
            return None

        miniterms = [miniterm]
        used_operators = []

        while self.lexer.current_token.type in [TokenType.MUL,
                                                TokenType.FLOAT_DIV,
                                                TokenType.INTEGER_DIV,
                                                TokenType.MODULO]:
            used_operators.append(self.lexer.current_token.type)
            self.lexer.build_next_token()
            miniterms.append(self.try_to_parse_miniterm())

        return Term(miniterms, used_operators)

    def try_to_parse_miniterm(self):
        unary_operator = None
        if self.lexer.current_token.type in [TokenType.PLUS,
                                             TokenType.MINUS,
                                             TokenType.NOT]:
            unary_operator = self.lexer.current_token.type
            self.lexer.build_next_token()
        if miniterm := self.try_to_parse_microterm():
            return MiniTerm(unary_operator, miniterm)
        return None

    def try_to_parse_microterm(self):
        if base := self.try_to_parse_factor() is None:
            return None
        power = None
        if self.lexer.current_token.type == TokenType.POW:
            self.lexer.build_next_token()
            power = self.try_to_parse_factor()
        return MicroTerm(base, power)

    def try_to_parse_factor(self):
        for try_to_parse_factor in [self.try_to_parse_constant,
                                    self.try_to_parse_non_constant,
                                    self.try_to_parse_expression_in_brackets]:
            if factor := try_to_parse_factor():
                return factor

    def try_to_parse_non_constant(self):
        if self.lexer.current_token.type != TokenType.ID:
            return None
        id = self.lexer.current_token.value
        self.lexer.build_next_token()

        for parse_method in [self.try_to_parse_id,
                             self.try_to_parse_function_call,
                             self.try_to_parse_matrix_subscripting]:
            if non_constant := parse_method(id):
                return non_constant
        return None

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

    def try_to_parse_constant(self):
        for parse_scalar in [self.try_to_parse_scalar,
                             self.try_to_parse_matrix]:
            if constant := parse_scalar():
                return constant
        return None

    def try_to_parse_scalar(self):
        if self.lexer.current_token.type != TokenType.SCALAR:
            return None
        scalar = Scalar(self.lexer.current_token())
        self.lexer.build_next_token()
        return scalar

    def try_to_parse_string(self):
        if self.lexer.current_token.type != TokenType.STRING:
            return None
        return String(self.lexer.current_token)

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

    def try_to_parse_matrix_row(self):
        expressions = [self.try_to_parse_expression()]

        while self.lexer.current_token.type == TokenType.COMMA:
            self.lexer.build_next_token()
            expressions.append(self.try_to_parse_expression())

        return MatrixRow(expressions)

    def try_to_parse_expression_in_brackets(self):
        if self.lexer.current_token.type != TokenType.LPAREN:
            return None
        self.lexer.build_next_token()
        expression = self.try_to_parse_expression()
        self.expect(TokenType.RPAREN)
        return expression

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
