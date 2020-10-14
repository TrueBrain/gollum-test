import html
import logging
import os
import wikitextparser

from typing import (
    Any,
    Dict,
)

log = logging.getLogger(__name__)


def process_wikilink_file(wikilink: wikitextparser.WikiLink, page: str):
    if not os.path.exists(f"data/uploads/{wikilink.title[5:]}"):
        log.error("[%s] Upload does not exist: %s", page, wikilink.title)
        file_not_found = True
    else:
        file_not_found = False

    url = html.escape(wikilink.title[5:]).strip()

    # TODO -- What is the default?
    title = ""
    options = {
        "height": None,
        "horizontal": None,
        "vertical": "middle",
        "width": None,
    }  # type: Dict[str, Any]
    thumb = False
    magnify = False

    if wikilink.text:
        # If there is any text, they are parameters divided by |
        raw_options = wikilink.text.split("|")

        for raw_option in raw_options:
            option = raw_option.lower().strip()

            if option in ("left", "center", "right", "none"):
                options["horizontal"] = option
            elif option in ("baseline", "sub", "super", "top", "text-top", "middle", "bottom", "text-bottom"):
                options["vertical"] = option
            elif option in ("thumb", "frame"):
                thumb = True
                if option == "thumb":
                    magnify = True
            elif option.endswith("px"):
                option = option[:-2]
                if "x" in option:
                    width, _, height = option.partition("x")
                    if width:
                        options["width"] = int(width)
                    options["height"] = int(height)
                else:
                    width = option
                    options["width"] = int(width)
            elif title == "":
                # Anything we don't understand has to be the title .. we hope
                title = raw_option.strip()
            else:
                # We cannot tell which of the two was meant to the the title.
                # So we leave it to the user to make that call.
                log.error("[%s] either %s or %s is not a valid option", page, title, option)
                # TODO -- Return error to user

    extra_a = ""
    extra_img = ""
    if title and not thumb:
        extra_a += f' title="{title}"'
        extra_img += f' alt="{title}"'

    if thumb:
        extra_img += ' class="thumbimage"'

    if options["width"]:
        extra_img += f' width="{options["width"]}"'
    if options["height"]:
        extra_img += f' height="{options["height"]}"'

    # Thumbs are by default floating right
    if thumb and options["horizontal"] is None:
        options["horizontal"] = "right"

    if file_not_found:
        content = "Image not found"
    else:
        content = f'<a href="/File:{url}" class="image"{extra_a}>'
        # TODO -- If thumb, load a thumb-url, not the full image
        content += f'<img src="/uploads/{url}"{extra_img} />'
        content += "</a>"

    if thumb:
        content += '<div class="thumbcaption">'
        if magnify:
            content += f'<div class="magnify"><a href="/File:{url}" class="internal" title="Enlarge">🔍</a></div>'
        content += f"{title}</div>\n"

        style = ""
        if options["width"]:
            style = f'width:{options["width"] + 2}px;'

        if style:
            style = f' style="{style}"'

        content = f'<div class="thumbinner"{style}>{content}</div>'
        if options["horizontal"] == "center":
            content = f'<div class="thumb tnone">{content}</div>'
            content = f'<div class="{options["horizontal"]}">{content}</div>'
        else:
            content = f'<div class="thumb t{options["horizontal"]}">{content}</div>'
    else:
        if options["horizontal"]:
            if options["horizontal"] == "center":
                content = f'<div class="floatnone">{content}</div>'
                content = f'<div class="{options["horizontal"]}">{content}</div>'
            else:
                content = f'<div class="float{options["horizontal"]}">{content}</div>'

    wikilink.string = content
