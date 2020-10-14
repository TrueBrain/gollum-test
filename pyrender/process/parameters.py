import wikitextparser

from typing import (
    List,
    Optional,
)


def process_parameters(wikitext: wikitextparser.WikiText, function_arguments: List[wikitextparser.Argument]):
    for parameter in reversed(wikitext.parameters):
        try:
            index = int(parameter.name) - 1  # type: Optional[int]
        except ValueError:
            index = None

        if index is not None:
            if index < len(function_arguments):
                # TODO -- Is "0" correct?
                value = function_arguments[index].value or "0"
            else:
                value = parameter.default or ""
        else:
            for function_argument in function_arguments:
                if function_argument.name.strip() == parameter.name:
                    value = function_argument.value
                    break
            else:
                value = parameter.default or ""

        parameter.string = value.strip()
