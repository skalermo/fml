from Source import TokenType
from Error import ParserError, ErrorCode
from Position import Position
from grammatical_objects.Program import Program
from grammatical_objects.Function import FunctionDefinition
from grammatical_objects.Statement import *
from grammatical_objects.Expression import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.program = self.parse_program()

    def expect(self, expected_token_type):
        if self.lexer.current_token.type != expected_token_type:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
        self.lexer.build_next_token()

    def parse_program(self):
        fun_defs = {}
        statements = []

        while (definition := self.try_to_parse_fun_definition()) or\
                (statement := self.parse_statement()):
            if definition is not None:
                fun_defs[definition.id] = definition
            elif statement is not None:
                statements.append(statement)

        return Program(fun_defs, statements)

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.build_next_token()

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        fun_id = self.lexer.current_token.value
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        parameter_list = self.try_to_parse_fun_parameters()

        if statement := self.parse_statement() is None:
            self.error(error_code=ErrorCode.EXPECTED_STATEMENT)

        return FunctionDefinition(fun_id, parameter_list, statement)

    def try_to_parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        self.lexer.build_next_token()

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

    def parse_statement(self):
        # Handle do_while_loop apart from other statements
        # because of the mandatory semi at the end
        if statement := self.try_to_parse_do_while_loop():
            if self.lexer.current_token.type != TokenType.SEMI:
                self.error(error_code=ErrorCode.EXPECTED_SEMI)
            return statement

        for try_to_parse_statement in [self.try_to_parse_while_loop,
                                       self.try_to_parse_for_loop,
                                       self.try_to_parse_if_statement,
                                       self.try_to_parse_compound_statement,
                                       self.try_to_parse_ret_statement,
                                       self.try_to_parse_expression]:
            if statement := try_to_parse_statement(self):
                return statement
        return None

    def try_to_parse_do_while_loop(self):
        if self.lexer.current_token.type != TokenType.DO:
            return None
        self.lexer.build_next_token()

        statement = self.parse_statement()

        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)

        logical_expr = self._generic_parser(ConditionExpression)

        self.expect(TokenType.RPAREN)

        return DoWhileLoop(statement, logical_expr)

    def try_to_parse_while_loop(self):
        if self.lexer.current_token.type != TokenType.WHILE:
            return None

        self.expect(TokenType.LPAREN)

        logical_expr = self._generic_parser(ConditionExpression)

        self.expect(TokenType.RPAREN)

        statement = self.parse_statement()
        return WhileLoop(statement, logical_expr)

    def try_to_parse_for_loop(self):
        pass

    def try_to_parse_if_statement(self):
        if self.lexer.current_token.type != TokenType.IF:
            return None
        self.lexer.build_next_token()

        self.expect(TokenType.LPAREN)

        cond_expr = self._generic_parser(ConditionExpression)

        self.expect(TokenType.RPAREN)

        statement = self.parse_statement()
        else_statement = None

        if self.lexer.current_token.type == TokenType.ELSE:
            self.lexer.build_next_token()
            else_statement = self.parse_statement()

        return IfStatement(cond_expr, statement, else_statement)

    def try_to_parse_compound_statement(self):
        if self.lexer.current_token != TokenType.LCURB:
            return None

        self.lexer.build_next_token()
        statement_list = []
        while self.lexer.current_token != TokenType.RCURB:
            if self.lexer.current_token == TokenType.ETX:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            if statement := self.parse_statement():
                statement_list.append(statement)

        self.lexer.build_next_token()
        return CompoundStatement(statement_list)

    def try_to_parse_ret_statement(self):
        if self.lexer.current_token.type != TokenType.RETURN:
            return None
        self.lexer.build_next_token()

        expression = self.try_to_parse_expression()

        if self.lexer.current_token.type != TokenType.SEMI:
            self.error(error_code=ErrorCode.EXPECTED_SEMI)
        return ReturnStatement(expression)

    def try_to_parse_expression(self):
        for try_to_parse_expression in [self.try_to_parse_assignment,
                                        self._generic_parser(ConditionExpression)]:
            if expression := try_to_parse_expression(self):
                return expression
        return None

    def try_to_parse_assignment(self):
        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        lhs = self.lexer.current_token.value
        self.lexer.build_next_token()

        self.expect(TokenType.EQ)

        if self.lexer.current_token.type == TokenType.STRING:
            # todo Make string an object to handle evaluate() call
            rhs = self.lexer.current_token.value
            return Assignment(lhs, rhs)

        rhs = self._generic_parser(ConditionExpression)
        return Assignment(lhs, rhs)

    def _generic_parser(self, ExpressionClass):
        if ExpressionClass is MiniTerm:
            return self.try_to_parse_miniterm()

        SubExpressionClass = subexpressions_and_binary_operators[ExpressionClass][0]
        operators = subexpressions_and_binary_operators[ExpressionClass][1]
        subexpressions = [self._generic_parser(SubExpressionClass)]
        used_operators = []

        while self.lexer.current_token.type in operators:
            used_operators.append(self.lexer.current_token.type)
            self.lexer.build_next_token()
            subexpressions.append(self._generic_parser(SubExpressionClass))

        return ExpressionClass(subexpressions, used_operators)

    def try_to_parse_miniterm(self):
        unary_operator = None
        if self.lexer.current_token.type in [TokenType.PLUS,
                                             TokenType.MINUS,
                                             TokenType.NOT]:
            unary_operator = self.lexer.current_token.type
            self.lexer.build_next_token()
        return MiniTerm(unary_operator, self.try_to_parse_microterm())

    def try_to_parse_microterm(self):
        base = self.try_to_parse_factor()
        if self.lexer.current_token.type == TokenType.POW:
            self.lexer.build_next_token()
            power = self.try_to_parse_factor()

    def try_to_parse_factor(self):
        pass

    def error(self, error_code=None):
        s = 'line: {position.line} column: {position.column}'.format(
            position=Position(self.lexer.source)
        )
        raise ParserError(error_code=error_code, message=s)

    # def try_to_parse_condition_expression(self):
    #     and_expressions = [self.try_to_parse_andExpression()]
    #
    #     while self.lexer.current_token.type == TokenType.OR:
    #         self.lexer.build_next_token()
    #         and_expressions.append(self.try_to_parse_andExpression())
    #
    #     return ConditionExpression(and_expressions)
    #
    # def try_to_parse_andExpression(self):
    #     equality_expressions = [self.try_to_parse_equality_expression()]
    #
    #     while self.lexer.current_token.type == TokenType.AND:
    #         self.lexer.build_next_token()
    #         equality_expressions.append(self.try_to_parse_equality_expression())
    #
    #     return AndExpression(equality_expressions)
    #
    # def try_to_parse_equality_expression(self):
    #     relative_expressions = [self.try_to_parse_relative_expression()]
    #     operators = []
    #
    #     while self.lexer.current_token.type in [TokenType.EQ,
    #                                             TokenType.NEQ]:
    #         operators.append(self.lexer.current_token.type)
    #         self.lexer.build_next_token()
    #         relative_expressions.append(self.try_to_parse_relative_expression())
    #
    #     return EqualityExpression(relative_expressions, operators)
    #
    # def try_to_parse_relative_expression(self):
    #     arithmetic_expressions = [self.try_to_parse_arithmetic_expression()]
    #     operators = []
    #
    #     while self.lexer.current_token.type in [TokenType.LEQ,
    #                                             TokenType.LESS,
    #                                             TokenType.GEQ,
    #                                             TokenType.GRE]:
    #         operators.append(self.lexer.current_token.type)
    #         self.lexer.build_next_token()
    #         arithmetic_expressions.append(self.try_to_parse_arithmetic_expression())
    #
    #     return RelativeExpression(arithmetic_expressions, operators)
    #
    # def try_to_parse_arithmetic_expression(self):
    #     terms = [self.try_to_parse_term()]
    #     operators = []
    #
    #     while self.lexer.current_token.type in [TokenType.PLUS,
    #                                             TokenType.MINUS]:
    #         operators.append(self.lexer.current_token.type)
    #         self.lexer.build_next_token()
    #         terms.append(self.try_to_parse_term())
    #
    #     return ArithmeticExpression(terms, operators)