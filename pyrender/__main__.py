import click
import logging
import wikitextparser

from aiohttp import web
from aiohttp.web_log import AccessLogger
from openttd_helpers import click_helper
from openttd_helpers.logging_helper import click_logging
from openttd_helpers.sentry_helper import click_sentry

from .process.bolds_and_italics import process_bolds_and_italics
from .process.comments import process_comments
from .process.external_links import process_external_links
from .process.lists import process_lists
from .process.parser_functions import process_parser_functions
from .process.sections import process_sections
from .process.tables import process_tables
from .process.templates import process_templates
from .process.wikilinks import process_wikilinks
from .write_html import (
    render_html,
    write_html,
)

log = logging.getLogger(__name__)


def load_page(category, language, page):
    with open(f"data/{category}/{language}/{page}.mediawiki") as fp:
        wtp = wikitextparser.parse(fp.read())

    page = f"{category}/{language}/{page}"

    process_comments(wtp)
    process_templates(wtp, page)

    # Reload the template, to make sure new external links are being picked up
    wtp = wikitextparser.parse(wtp.string)

    process_parser_functions(wtp, page)
    process_bolds_and_italics(wtp)
    process_external_links(wtp)
    process_wikilinks(wtp, page)

    process_tables(wtp)
    process_lists(wtp)
    process_sections(wtp)

    return wtp.string


def render_all(language, skip_till_page):
    import glob

    def iterate(folder):
        for file in sorted(glob.glob(f"{folder}/*")):
            if file.endswith(".mediawiki"):
                category, language, page = file[5:].split("/", 2)
                page = page.rsplit(".", 1)[0]

                if skip_till_page is not None and page < skip_till_page:
                    continue

                print(f"Loading {category}:{page} in {language} ...")
                load_page(category, language, page)
            else:
                iterate(file)

    def load_all(category, language):
        iterate(f"data/{category}/{language}")

    load_all("Main", language)


routes = web.RouteTableDef()


class ErrorOnlyAccessLogger(AccessLogger):
    def log(self, request, response, time):
        # Only log if the status was not successful
        if not (200 <= response.status < 400):
            super().log(request, response, time)


@routes.get("/{category}/{language}/{page:.*}")
async def main_handler(request):
    category = request.match_info["category"]
    language = request.match_info["language"]
    page = request.match_info["page"]

    body = render_html(category, language, page, load_page(category, language, page))
    return web.Response(body=body, content_type="text/html")


@routes.route("*", "/{tail:.*}")
async def fallback(request):
    log.warning("Unexpected URL: %s", request.url)
    return web.HTTPNotFound()


def run_server():
    webapp = web.Application()
    webapp.router.add_static("/uploads", "data/uploads/")
    webapp.router.add_static("/css", "data/css/")
    webapp.add_routes(routes)

    web.run_app(webapp, host="127.0.0.1", port=8000, access_log_class=ErrorOnlyAccessLogger)


@click_helper.command()
@click_logging  # Should always be on top, as it initializes the logging
@click_sentry
@click.option("--category", help="Category of the page to render", show_default=True, default="Main")
@click.option("--language", help="Language of the page to render", show_default=True, default="en")
@click.option("--check-all", help="Check all pages if they would render, and report any errors", is_flag=True)
@click.option("--server", help="Start a webserver; highly experimental", is_flag=True)
@click.argument("page", required=False)
def main(category, language, page, check_all, server):
    if check_all:
        render_all(language, page)
        return

    if server:
        run_server()
        return

    body = load_page(category, language, page)
    write_html(category, language, page, body)


if __name__ == "__main__":
    main()
