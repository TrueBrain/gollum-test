import html
import wikitextparser

from html.parser import HTMLParser
from slugify import slugify

VALID_TAGS = (
    "a",
    "b",
    "big",
    "blockquote",
    "br",
    "caption",
    "center",
    "code",
    "dd",
    "div",
    "dl",
    "dt",
    "em",
    "font",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "tr",
    "tt",
    "u",
    "ul",
)

BLOCK_ELEMENTS = (
    "center",
    "dd",
    "div",
    "dl",
    "dt",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "ol",
    "p",
    "pre",
    "table",
    "ul",
)


class ChainHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._result = ""
        self._has_ended = False

    def feed(self, feed: str):
        super().feed(feed)
        return self

    def handle_entityref(self, name):
        self._result += f"&{name};"

    def handle_charref(self, name):
        self._result += f"&#{name};"

    def unknown_decl(self, data):
        raise NotImplementedError(f"Unknown data in output: {data}")

    def get_endtag_text(self, tag):
        return f"</{tag}>"

    def handle_eof(self):
        pass

    @property
    def result(self):
        if not self._has_ended:
            self._has_ended = True
            self.handle_eof()

        return self._result


class ReplaceUnknownTags(ChainHTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag not in VALID_TAGS:
            self._result += html.escape(self.get_starttag_text(), quote=False)
        elif tag == "br":
            # Replace <br> with <br/>; this makes other passes easier
            self._result += "<br />"
        else:
            self._result += self.get_starttag_text()

    def handle_startendtag(self, tag, attrs):
        if tag not in VALID_TAGS:
            self._result += html.escape(self.get_starttag_text(), quote=False)
        else:
            self._result += self.get_starttag_text()

    def handle_endtag(self, tag):
        if tag not in VALID_TAGS:
            self._result += html.escape(self.get_endtag_text(tag), quote=False)
        else:
            self._result += self.get_endtag_text(tag)

    def handle_data(self, data):
        self._result += data


class AddPreBlocks(ChainHTMLParser):
    def __init__(self):
        super().__init__()
        self._tag_count = 0
        self._pre_open = False

    def handle_starttag(self, tag, attrs):
        self._tag_count += 1
        self._result += self.get_starttag_text()

    def handle_startendtag(self, tag, attrs):
        self._result += self.get_starttag_text()

    def handle_endtag(self, tag):
        self._tag_count -= 1
        self._result += self.get_endtag_text(tag)

    def handle_data(self, data):
        if self._tag_count != 0:
            self._result += data
            return

        for line in data.split("\n"):
            if not self._result or self._result[-1] == "\n":
                if line and line[0] == " ":
                    if not self._pre_open:
                        self._pre_open = True
                        self._result += "<pre>"
                else:
                    if self._pre_open:
                        self._pre_open = False
                        self._result = self._result[:-1]
                        self._result += "</pre>\n"

            self._result += line + "\n"

        self._result = self._result[:-1]


class AddPBlocks(ChainHTMLParser):
    def __init__(self):
        super().__init__()
        self._block_depth = 0
        self._p_open = False

    def handle_starttag(self, tag, attrs):
        if tag in BLOCK_ELEMENTS:
            self._block_depth += 1

            if self._p_open:
                self._p_open = False
                self._result += "</p>"

        self._result += self.get_starttag_text()

    def handle_startendtag(self, tag, attrs):
        self._result += self.get_starttag_text()

    def handle_endtag(self, tag):
        if tag in BLOCK_ELEMENTS:
            self._block_depth -= 1

            if self._p_open:
                self._p_open = False
                self._result += "</p>"

        self._result += self.get_endtag_text(tag)

    def handle_data(self, data):
        if self._block_depth == 0 and not self._p_open:
            self._p_open = True
            self._result += "<p>"

        if self._p_open:
            data = data.replace("\n\n", "</p>\n<p>")

        self._result += data

    def handle_eof(self):
        if self._p_open:
            self._p_open = False
            self._result += "</p>"

        self._result = self._result.replace("<p></p>", "").replace("<p>\n</p>", "")


def process_sections(wikitext: wikitextparser.WikiText):
    for section in reversed(wikitext.get_sections()):
        if not section:
            continue

        contents = section.contents
        contents = ReplaceUnknownTags().feed(contents).result
        contents = AddPreBlocks().feed(contents).result
        contents = AddPBlocks().feed(contents).result

        if section.title:
            slug = slugify(section.title.strip())

            content = f"<h{section.level}>"
            content += f'<a class="anchor" id="{slug}" href="#{slug}"></a>'
            content += f'<a name="{slug}" id="{slug}"></a>'
            content += f'<span class="mw-headline" id="{slug}">{section.title.strip()}</span>'
            content += f"</h{section.level}>\n"
        else:
            content = ""

        section.string = content + contents
