import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount


def process_pf_namespace(parser_function: wikitextparser.ParserFunction, page: str):
    if len(parser_function.arguments) != 0:
        raise ParserFunctionWrongArgumentCount

    parser_function.string = page.split("/")[0]
