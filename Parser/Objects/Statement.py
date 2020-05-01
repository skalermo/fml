from Interpreter.Ast import AST


class Executable(AST):
    pass


class Statement(Executable):
    pass


class ReturnStatement(Statement):
    def __init__(self, expression_to_return):
        self.expression = expression_to_return

    def __repr__(self):
        return f'{self.__class__.__name__}'


class ForLoop(Statement):
    def __init__(self, iterator, iterable, statement):
        self.iterator = iterator
        self.iterable = iterable
        self.statement = statement

    def __repr__(self):
        return f'{self.__class__.__name__}'


class WhileLoop(Statement):
    def __init__(self, statement, condition_expression):
        self.condition_expression = condition_expression
        self.statement = statement

    def __repr__(self):
        return f'{self.__class__.__name__}'


class DoWhileLoop(WhileLoop):
    pass


class IfStatement(Statement):
    def __init__(self, conditional_expression, statement, else_statement: [Statement, None]):
        self.conditional_expression = conditional_expression
        self.statement = statement
        self.else_statement = else_statement

    def __repr__(self):
        return f'{self.__class__.__name__}'


class CompoundStatement(Statement):
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def __repr__(self):
        return f'{self.__class__.__name__}'


class EmptyStatement(Statement):
    def __repr__(self):
        return f'{self.__class__.__name__}'
