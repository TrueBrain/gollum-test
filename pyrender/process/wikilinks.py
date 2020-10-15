import wikitextparser

from .wikilink.internal import process_wikilink_internal
from .wikilink.file import process_wikilink_file
from .wikilink.translation import process_wikilink_translation


def process_wikilinks(wikitext: wikitextparser.WikiText, page: str):
    for wikilink in reversed(wikitext.wikilinks):
        # TODO -- Remove hardcoded entries, including "AI:"
        if (
            ":" not in wikilink.title
            or wikilink.title.startswith("Main/en/AI:")
            or wikilink.title.startswith("Main/fr/IA:")
            or wikilink.title.startswith("Main/en/IA:")
            or wikilink.title.startswith("Main/en/SI:")
            or wikilink.title.startswith("Main/pl/SI:")
            or wikilink.title.startswith("Main/es/IA:")
            or wikilink.title.startswith("Main/fi/AI:")
            or wikilink.title
            in (
                "Main/en/Road Construction:Old",
                "Main/en/SimCity 2000: Special Edition Music Set",
                "Main/en/Tycoonez.com:munity Czech Sets",
                "Main/fr/Signalisation du réseau ferroviaire : agencements complexes",
                "Main/en/Signalisation du réseau ferroviaire : agencements complexes/Fr",
                "Main/fr/Ensembles tchèques Tycoonez.com:munity",
                "Main/fr/Signalisation du réseau ferroviaire : options et fonctionnalités avancées",
                "Main/nl/Nu een andere routegebaseerde signaleringpatch : YAPP",
            )
        ):
            process_wikilink_internal(wikilink, page)
        elif wikilink.title.startswith("File:"):
            process_wikilink_file(wikilink, page)
        elif wikilink.title.startswith("Translation:"):
            process_wikilink_translation(wikilink)
        elif wikilink.title.startswith("Category:") or wikilink.title.startswith("Main/en/Kategorie:"):
            # TODO -- Implement
            wikilink.string = ""
        elif wikilink.title.startswith("Media:"):
            # TODO -- Implement
            wikilink.string = ""
        elif wikilink.title.startswith("Template:"):
            # TODO -- Implement
            wikilink.string = ""
        elif wikilink.title.startswith("Main/en/Special:") or wikilink.title.startswith("Main/en/special:"):
            # TODO -- Figure out what we want with this
            wikilink.string = ""
        elif wikilink.title.startswith("Archive/"):
            # TODO -- Check with frosch what the idea is here
            wikilink.string = ""
        elif wikilink.title.startswith("OpenTTD:"):
            # TODO -- Check with frosch where these pages went to
            wikilink.string = ""
        elif wikilink.title == "Main/en/Image:No_image.png":
            # Here something went a bit wrong, comes from "Finished 32bpp Graphics ExtraZoom"
            wikilink.string = ""
        elif wikilink.title.startswith("Main/en/Image:") or wikilink.title.startswith("Wikipedia:") or wikilink.title.startswith("Image:"):
            # TODO -- Wrongly converted link
            wikilink.string = ""
        elif wikilink.title in (
            "YAPP/Nl#Basic single track",
            "Main/en/Nu een andere routegebaseerde signaleringpatch : YAPP/Nl#Basic single track",
        ):
            # TODO -- Export missed the #, and didn't fix the link
            wikilink.string = ""
        elif wikilink.title.startswith("Main/en/Main talk:") or wikilink.title.startswith("Main/en/Main:"):
            # TODO -- {{NAMESPACE}} URLs that got prefixed with "Main/en"
            wikilink.string = ""
        else:
            raise NotImplementedError(f"Unknown WikiLink {wikilink.title}")
