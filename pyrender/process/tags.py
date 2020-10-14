import wikitextparser


def process_tags(wikitext: wikitextparser.WikiText):
    for tag in reversed(wikitext.get_tags()):
        if tag.name == "noinclude":
            tag.string = ""
        elif tag.name == "includeonly":
            tag.string = tag.contents
        elif tag.name == "nowiki":
            # TODO -- Implement this
            pass
        elif tag.name in (
            "b",
            "big",
            "br",
            "center",
            "code",
            "div",
            "font",
            "p",
            "pre",
            "small",
            "span",
            "strong",
            "sub",
            "table",
            "td",
            "th",
            "tr",
        ):
            # Valid HTML code, so leave it unchanged
            pass
        elif tag.name == "gallery":
            # TODO -- Figure out if this really exists
            pass
        else:
            raise NotImplementedError(f"Unknown tag {tag.name}")
