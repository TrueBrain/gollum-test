import wikitextparser

from .parser_function import (
    expr,
    if_,
    ifeq,
    ifexpr,
    switch,
    pagename,
    namespace,
)


PARSER_FUNCTIONS = {
    "#expr": expr.process_pf_expr,
    "#if": if_.process_pf_if,
    "#ifeq": ifeq.process_pf_ifeq,
    "#ifexpr": ifexpr.process_pf_ifexpr,
    "#switch": switch.process_pf_switch,

    "pagename": pagename.process_pf_pagename,
    "namespace": namespace.process_pf_namespace,
}


def process_parser_functions(wikitext: wikitextparser.WikiText, page: str):
    for parser_function in reversed(wikitext.parser_functions):
        name = parser_function.name.lower().strip()

        if name in PARSER_FUNCTIONS:
            PARSER_FUNCTIONS[name](parser_function, page)
        elif name in ("fullurl", "localurl", "ucfirst", "lc", "talkpagename", "server", "currentyear", "displaytitle"):
            # TODO -- Implement this
            parser_function.string = ""
        else:
            raise NotImplementedError(f"Unknown parser function {parser_function.name}")
