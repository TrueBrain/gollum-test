import wikitextparser


def get_argument(parser_function: wikitextparser.ParserFunction, index: int):
    if len(parser_function.arguments) <= index:
        return ""
    return parser_function.arguments[index].string[1:].strip()
