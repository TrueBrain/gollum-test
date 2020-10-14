import html
import logging
import os
import wikitextparser

log = logging.getLogger(__name__)


def process_wikilink_internal(wikilink: wikitextparser.WikiLink, page: str):
    title = wikilink.title.strip()
    pagename = "/".join(title.split("/")[2:])

    if wikilink.text is None:
        text = pagename
    else:
        text = wikilink.text.strip()

    link_extra = ""

    if not os.path.exists(f"data/{title.partition('#')[0]}.mediawiki"):
        log.error("[%s] Page does not exist: %s", page, title)
        link_extra = ' class="new"'

    if title == page:
        wikilink.string = f'<strong class="selflink">{text}</strong>'
    else:
        wikilink.string = f'<a href="/{html.escape(title)}"{link_extra} title="{pagename}">{text}</a>'
