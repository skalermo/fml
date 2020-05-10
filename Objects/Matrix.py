from Interpreter.Ast import AST


class Matrix(AST):
    def __init__(self, rows):
        self.rows = rows

    def __getitem__(self, item):
        return self.rows[item]

    def __len__(self):
        return sum([len(row) for row in self.rows])

    def __repr__(self):
        return f'{self.__class__.__name__}'


class MatrixRow:
    def __init__(self, expressions):
        self.expressions = expressions

    def __getitem__(self, item):
        return self.expressions[item]

    def __len__(self):
        return len(self.expressions)


class MatrixIndex(AST):
    def __init__(self, expression, is_colon=False):
        self.expression = expression
        self.is_colon = is_colon

    def __repr__(self):
        return f'{self.__class__.__name__}'


class MatrixSubscripting(AST):
    def __init__(self, id, idx, idx2):
        self.id = id
        self.row_index = idx
        self.column_index = idx2

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.value}'
