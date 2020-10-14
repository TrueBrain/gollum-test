import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helper import get_argument


def process_pf_ifeq(parser_function: wikitextparser.ParserFunction, page: str):
    if len(parser_function.arguments) < 2:
        raise ParserFunctionWrongArgumentCount

    left = get_argument(parser_function, 0)
    right = get_argument(parser_function, 1)

    if left == right:
        parser_function.string = get_argument(parser_function, 2)
    else:
        parser_function.string = get_argument(parser_function, 3)
