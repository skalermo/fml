class Matrix:
    def __init__(self, rows):
        self.rows = rows

    def __getitem__(self, item):
        return self.rows[item]

    def __len__(self):
        return len(self.rows)


class MatrixRow:
    def __init__(self, expressions):
        self.expressions = expressions

    def __getitem__(self, item):
        return self.expressions[item]

    def __len__(self):
        return len(self.expressions)


class MatrixIndex:
    def __init__(self, expression, is_colon=False):
        self.expression = expression
        self.is_colon = is_colon


class MatrixSubscripting:
    def __init__(self, id, idx, idx2):
        self.id = id
        self.row_index = idx
        self.column_index = idx2
