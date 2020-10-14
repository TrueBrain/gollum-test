import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helper import get_argument


def process_pf_if(parser_function: wikitextparser.ParserFunction, page: str):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    condition = get_argument(parser_function, 0)

    if condition:
        parser_function.string = get_argument(parser_function, 1)
    else:
        parser_function.string = get_argument(parser_function, 2)
