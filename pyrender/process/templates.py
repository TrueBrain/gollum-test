import logging
import wikitextparser

from typing import List

from .comments import process_comments
from .parameters import process_parameters
from .parser_functions import process_parser_functions
from .tags import process_tags

log = logging.getLogger(__name__)


def load_template(template: wikitextparser.Template, function_arguments: List[wikitextparser.Argument], page: str):
    try:
        with open(f"data/{template}.mediawiki") as fp:
            wtp = wikitextparser.parse(fp.read())
    except FileNotFoundError:
        log.error("[%s] Template not found: %s", page, template)
        return f"Template {template} not found"

    process_comments(wtp)
    process_tags(wtp)
    process_parameters(wtp, function_arguments)
    process_parser_functions(wtp, page)
    process_templates(wtp, page)

    return wtp.string


def process_templates(wikitext: wikitextparser.WikiText, page: str):
    for template in reversed(wikitext.templates):
        name = template.name.strip()

        if ":" not in name:
            template.string = load_template(f"Template/{name}", template.arguments, page)
        elif name.startswith("Template:") or name.startswith("template:"):
            # TODO -- "Template" should already been removed by the conversion
            log.info("[%s] Template namespace used: %s", page, name)
            if name[0] == ":":
                name = name[1:]
            name = name.split(":", 1)[1]
            template.string = load_template(f"Template/en/{name}", template.arguments, page)
        elif name.startswith(":Scenario:") or name.startswith("Scenario:") or name.startswith("scenario:"):
            # TODO -- "Scenario" should already been removed by the conversion
            log.info("[%s] Scenario namespace used: %s", page, name)
            if name[0] == ":":
                name = name[1:]
            name = name.split(":", 1)[1]
            template.string = load_template(f"Scenario/en/{name}", template.arguments, page)
        elif name.startswith(":Links/") or name.startswith(":Liens/"):
            # TODO -- "Links" should already been removed by the conversion
            log.info("[%s] Links namespace used: %s", page, name)
            template.string = ""
        elif name in (
            ":Settings/Graph",
            ":Settings/Zoom",
            ":Settings/Graph line thickness",
            ":Settings/Dynamic Engines",
            ":Settings/Road vehicle slope steepness",
            ":Settings/Road vehicle acceleration model",
        ):
            # TODO -- "Settings" should already been removed by the conversion
            log.info("[%s] Settings namespace used: %s", page, name)
            # "Advanced Settings/Interface" includes these pages, which are not templates
            template.string = ""
        else:
            raise NotImplementedError(f"Unknown template {name}")
