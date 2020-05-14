from Interpreter.Ast import AST


class Matrix(AST):
    def __init__(self, rows):
        self.rows = rows
        # shape = (rows, columns)
        self.shape = (len(rows), 0 if not rows else len(rows[0]))

    def __getitem__(self, item):
        if item >= self.shape[0]:
            return None
        return self.rows[item]

    def __setitem__(self, key, value):
        self.rows[key] = value

    def __len__(self):
        return self.shape[0] * self.shape[1]

    def __str__(self):
        return f'{self.__class__.__name__}'

    def to_py(self):
        return [row.to_py() for row in self.rows]

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

    def get_item_by_single_idx(self, idx):
        if idx >= len(self) or idx < 0:
            return None
        rowno = idx // self.shape[1]
        colno = idx % self.shape[1]
        return self.rows[rowno][colno]

    def get_shape(self):
        return Matrix([list(self.shape)])

    def get_row(self, idx):
        if idx >= self.shape[0] or idx < 0:
            return None
        return Matrix([self.rows[idx]])

    def get_column(self, idx):
        if idx >= self.shape[1] or idx < 0:
            return None
        return Matrix([MatrixRow([row[idx] for row in self.rows])])

    def copy(self):
        return Matrix(self.rows[:])


class MatrixRow:
    def __init__(self, expressions):
        self.elements = expressions

    def __getitem__(self, item):
        if item >= len(self):
            return None
        return self.elements[item]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __len__(self):
        return len(self.elements)

    def __bool__(self):
        return bool(len(self))

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __eq__(self, other):
        pass

    def to_py(self):
        return [expression.to_py() for expression in self.elements]

    def append(self, param):
        self.elements.append(param)


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
