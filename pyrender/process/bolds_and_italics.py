import wikitextparser


def process_bolds_and_italics(wikitext: wikitextparser.WikiText):
    for bold in reversed(wikitext.get_bolds(recursive=False)):
        bold.string = f"<b>{bold.text.strip()}</b>"

    for italic in reversed(wikitext.get_italics(recursive=False)):
        italic.string = f"<i>{italic.text.strip()}</i>"
