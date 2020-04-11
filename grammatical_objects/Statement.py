class Statement:
    pass


class DoWhileLoop(Statement):
    pass


class WhileLoop(Statement):
    pass


class IfStatement(Statement):
    pass


class CompoundStatement(Statement):
    def __init__(self, statement_list):
        self.statement_list = statement_list
