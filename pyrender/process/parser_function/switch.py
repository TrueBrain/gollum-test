import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helper import get_argument


def process_pf_switch(parser_function: wikitextparser.ParserFunction, page: str):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    branch = get_argument(parser_function, 0)

    # TODO -- What is the correct default value?
    default = ""

    for argument in parser_function.arguments[1:]:
        if argument.name.strip() == "#default":
            default = argument.value

        if argument.name.strip() == branch:
            parser_function.string = argument.value
            break
    else:
        parser_function.string = default
