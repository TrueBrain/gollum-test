import html
import wikitextparser


def process_external_links(wikitext: wikitextparser.WikiText):
    for external_link in reversed(wikitext.external_links):
        url = html.escape(external_link.url.strip())
        if external_link.text:
            text = external_link.text.strip()
        else:
            text = url

        external_link.string = f'<a class="external text" href="{url}">{text}</a>'
