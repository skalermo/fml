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
    SEMI = ';'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = '*'
    FLOAT_DIV = '/'
    ASSIGN = '='
    LPAREN = '('
    RPAREN = ')'
    LESS = '<'
    GRE = '>'

    # other types
    LEQ = '<='
    GEQ = '>='
    EQ = '=='
    NEQ = '!='
    POW = 'POW'
    SCALAR = 'SCALAR'
    STRING = 'STRING'
    MATRIX = 'MATRIX'
    ID = 'ID'
    EOF = 'EOF'


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
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
