import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helper import get_argument


def process_pf_expr(parser_function: wikitextparser.ParserFunction, page: str):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    expr = get_argument(parser_function, 0)

    # TODO -- This is really unsafe, and needs rework!
    expr = expr.replace("round 0", "")
    try:
        parser_function.string = str(eval(expr))
    except Exception:
        parser_function.string = ""
