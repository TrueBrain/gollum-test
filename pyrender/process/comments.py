import wikitextparser


def process_comments(wikitext: wikitextparser.WikiText):
    for comment in reversed(wikitext.comments):
        comment.string = ""
