import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helper import get_argument


def process_pf_ifexpr(parser_function: wikitextparser.ParserFunction, page: str):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    condition = get_argument(parser_function, 0)

    # TODO -- This is really unsafe, and needs rework!
    try:
        result = eval(condition)
    except Exception:
        result = ""

    if result:
        parser_function.string = get_argument(parser_function, 1)
    else:
        parser_function.string = get_argument(parser_function, 2)
