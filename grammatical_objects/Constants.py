class Scalar:
    def __init__(self, token):
        self.value = token.value
        self.position = token.position


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
