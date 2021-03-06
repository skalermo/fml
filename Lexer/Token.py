from enum import Enum


class TokenType(Enum):
    # 13 reserved keywords
    AND = 'and'
    INTEGER_DIV = 'div'
    DO = 'do'
    ELSE = 'else'
    FOR = 'for'
    FUN = 'fun'
    IF = 'if'
    IN = 'in'
    MODULO = 'mod'
    NOT = 'not'
    OR = 'or'
    RETURN = 'ret'
    WHILE = 'while'

    # single-character token types
    ETX = '\x03'
    LPAREN = '('
    RPAREN = ')'
    LBRACK = '['
    RBRACK = ']'
    LCURB = '{'
    RCURB = '}'
    SEMI = ';'
    COMMA = ','
    COLON = ':'
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    ASSIGN = '='
    LESS = '<'
    GRE = '>'

    # other types
    LEQ = '<='
    GEQ = '>='
    EQ = '=='
    NEQ = '!='
    POW = '**'
    SCALAR = 'SCALAR'
    STRING = 'STRING'
    MATRIX = 'MATRIX'
    ID = 'ID'


def _build_reserved_keywords():
    """
    Build a dictionary of reserved keywords.
    Function takes advantage of fact that
    first 13 fields of class TokenTyp are reserved keywords.
    :return:
    """

    token_types_list = list(TokenType)
    reserved_keywords = {
        token_type.value: token_type
        for token_type in token_types_list[:13]
    }
    return reserved_keywords


RESERVED_KEYWORDS = _build_reserved_keywords()


class Token:
    def __init__(self, type, value=None, position=None):
        self.type = type
        if value is None:
            value = type.value
        self.value = value
        self.position = position

    def __str__(self):
        """
        String representation of the class instance.
        """
        return 'Token({type}, {value}, {position})'.format(
            type=self.type,
            value=repr(self.value),
            position=repr(self.position)
        )

    def __repr__(self):
        return self.__str__()
