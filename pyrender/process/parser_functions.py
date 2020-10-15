import wikitextparser

from .parser_function import (
    expr,
    if_,
    ifeq,
    ifexpr,
    namespace,
    pagename,
    switch,
)


PARSER_FUNCTIONS = {
    "#expr": expr.process_pf_expr,
    "#if": if_.process_pf_if,
    "#ifeq": ifeq.process_pf_ifeq,
    "#ifexpr": ifexpr.process_pf_ifexpr,
    "#switch": switch.process_pf_switch,
    "namespace": namespace.process_pf_namespace,
    "pagename": pagename.process_pf_pagename,
}


def process_parser_functions(wikitext: wikitextparser.WikiText, page: str):
    for parser_function in reversed(wikitext.parser_functions):
        name = parser_function.name.lower().strip()

        if name in PARSER_FUNCTIONS:
            PARSER_FUNCTIONS[name](parser_function, page)
        elif name in (
            "currentyear",
            "displaytitle",
            "fullpagename",
            "fullurl",
            "lc",
            "localurl",
            "server",
            "talkpagename",
            "ucfirst",
        ):
            # TODO -- Implement this
            parser_function.string = ""
        else:
            raise NotImplementedError(f"Unknown parser function {parser_function.name}")
