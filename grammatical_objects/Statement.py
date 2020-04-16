class Statement:
    pass


class ReturnStatement:
    def __init__(self, expression_to_return):
        self.expr = expression_to_return


class DoWhileLoop(Statement):
    pass


class WhileLoop(Statement):
    pass


class IfStatement(Statement):
    pass


class CompoundStatement(Statement):
    def __init__(self, statement_list):
        self.statement_list = statement_list
