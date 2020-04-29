class Executable:
    pass


class Statement(Executable):
    pass


class ReturnStatement(Statement):
    def __init__(self, expression_to_return):
        self.expression = expression_to_return


class ForLoop(Statement):
    def __init__(self, token_iterator, iterable, statement):
        self.token_iterator = token_iterator
        self.iterable = iterable
        self.statement = statement


class WhileLoop(Statement):
    def __init__(self, statement, logical_expression):
        self.statement = statement
        self.logical_expression = logical_expression


class DoWhileLoop(WhileLoop):
    pass


class IfStatement(Statement):
    def __init__(self, logical_expression, statement, else_statement: [Statement, None]):
        self.logical_expression = logical_expression
        self.statement = statement
        self.else_statement = else_statement


class CompoundStatement(Statement):
    def __init__(self, statement_list):
        self.statement_list = statement_list


class EmptyStatement(Statement):
    pass
