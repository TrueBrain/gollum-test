import wikitextparser


def process_wikilink_translation(wikilink: wikitextparser.WikiLink):
    page = wikilink.title.partition(":")[2]
    with open(f"data/.translation/{page}.html") as fp:
        wikilink.string = fp.read()
