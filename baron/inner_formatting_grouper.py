from utils import FlexibleIterator

BOTH = (
    "AS",
    "IMPORT",
    "DOUBLE_STAR",
    "DOT",
    "LEFT_SQUARE_BRACKET",
    "LEFT_PARENTHESIS",
    "STAR",
    "SLASH",
    "PERCENT",
    "DOUBLE_SLASH",
    "PLUS",
    "MINUS",
    "LEFT_SHIFT",
    "RIGHT_SHIFT",
    "AMPER",
    "CIRCUMFLEX",
    "VBAR",
    "LESS",
    "GREATER",
    "EQUAL_EQUAL",
    "LESS_EQUAL",
    "GREATER_EQUAL",
    "LESS_GREATER",
    "NOT_EQUAL",
    "IN",
    "IS",
    "NOT",
    "AND",
    "OR",
    "IF",
    "ELSE",
    "EQUAL",
    "PLUS_EQUAL",
    "MINUS_EQUAL",
    "STAR_EQUAL",
    "SLASH_EQUAL",
    "PERCENT_EQUAL",
    "AMPER_EQUAL",
    "VBAR_EQUAL",
    "CIRCUMFLEX_EQUAL",
    "LEFT_SHIFT_EQUAL",
    "RIGHT_SHIFT_EQUAL",
    "DOUBLE_STAR_EQUAL",
    "DOUBLE_SLASH_EQUAL",
    "ENDL",
    "COMMA",
    "FOR",
    "COLON"
)

GROUP_SPACE_BEFORE = BOTH + (
    "RIGHT_PARENTHESIS",
    "COMMENT",
)

GROUP_SPACE_AFTER = BOTH + (
    "FROM",
    "TILDE",
    "RETURN",
    "YIELD",
    "WITH",
    "DEL",
    "ASSERT",
    "RAISE",
    "EXEC",
    "GLOBAL",
    "PRINT",
    "INDENT",
    "WHILE",
    "ELIF",
    "EXCEPT",
    "DEF",
    "CLASS",
    "LAMBDA",
)

def group(sequence):
    return list(group_generator(sequence))


def group_generator(sequence):
    iterator = FlexibleIterator(sequence)
    current = None, None
    while True:
        if iterator.end():
            return

        current = iterator.next()

        if current is None:
            return

        yield current