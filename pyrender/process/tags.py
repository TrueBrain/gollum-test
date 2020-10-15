import wikitextparser

from .sections import VALID_TAGS


def process_tags(wikitext: wikitextparser.WikiText):
    for tag in reversed(wikitext.get_tags()):
        if tag.name == "noinclude":
            tag.string = ""
        elif tag.name == "includeonly":
            tag.string = tag.contents
        elif tag.name == "nowiki":
            # TODO -- Implement this
            pass
        elif tag.name in VALID_TAGS:
            # Valid HTML code, so leave it unchanged
            pass
        elif tag.name == "gallery":
            # TODO -- Figure out if this really exists
            pass
        else:
            raise NotImplementedError(f"Unknown tag {tag.name}")
