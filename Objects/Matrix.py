from Interpreter.Ast import AST


class Matrix(AST):
    def __init__(self, rows):
        self.rows = rows
        # shape = (rows, columns)
        self.shape = (len(rows), 0 if not rows else len(rows[0]))

    def __getitem__(self, item):
        return self.rows[item]

    def __len__(self):
        return self.shape[0] * self.shape[1]

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __bool__(self):
        return bool(len(self))

    def __eq__(self, other):
        if self.shape != other.shape:
            return False
        for row1, row2 in zip(self.rows, other.rows):
            for elem1, elem2 in zip(row1, row2):
                if elem1 != elem2:
                    return False
        return True


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
