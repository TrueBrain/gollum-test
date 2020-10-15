import html
import wikitextparser


def process_tables(wikitext: wikitextparser.WikiText):
    for table in reversed(wikitext.get_tables()):
        process_tables(table)

        table_style = ""
        table_extra = ""
        for attr, value in table.attrs.items():
            if attr == "style":
                style = html.escape(value, quote=False).replace('"', "'").strip()
                if not style:
                    raise RuntimeError(f"Table attribute {attr} has an empty value, which was not expected")

                if style[-1] != ";":
                    style += ";"
                table_style += f"{style} "
            elif attr in (
                "align",
                "bgcolor",
                "border",
                "bordercolor",
                "cellpadding",
                "cellspacing",
                "class",
                "padding",
                "rules",
                "width",
            ):
                value = html.escape(value).strip()
                if not value:
                    raise RuntimeError(f"Table attribute {attr} has an empty value, which was not expected")
                table_extra += f' {attr}="{value}"'
            else:
                raise NotImplementedError(f"Table attribute {attr} not yet implemented")

        if table_style:
            table_style = f' style="{table_style[:-1]}"'

        content = f"<table{table_style}{table_extra}>\n"
        if table.caption:
            content += f"<caption>{table.caption}\n</caption>\n"
        content += "<tbody>\n"

        skip_cells = 0
        # XXX -- Currently setting "span" to False bugs out; so we deduplicate ourself (skip_cells)
        for row in table.cells(span=True):
            content += "<tr>\n"
            for cell in row:
                if cell is None:
                    continue

                if skip_cells > 0:
                    skip_cells -= 1
                    continue

                cell_style = ""
                cell_extra = ""

                for attr, value in cell.attrs.items():
                    if attr == "colspan":
                        cell_extra += f' colspan="{value}"'
                        skip_cells = int(value) - 1
                    elif attr == "rowspan":
                        cell_extra += f' rowspan="{value}"'
                        # TODO -- What to skip?
                        # skip_cells = int(value) - 1
                    elif attr == "style":
                        style = html.escape(value, quote=False).replace('"', "'").strip()
                        if not style:
                            raise RuntimeError(f"Cell attribute {attr} has an empty value, which was not expected")

                        if style[-1] != ";":
                            style += ";"
                        cell_style += f"{style} "
                    elif attr in ("align", "bgcolor", "class", "height", "scope", "valign", "width"):
                        value = html.escape(value).strip()
                        if not value:
                            raise RuntimeError(f"Cell attribute {attr} has an empty value, which was not expected")
                        cell_extra += f' {attr}="{value}"'
                    elif attr in ("nowrap",):
                        cell_extra += f" {attr}"
                    else:
                        raise NotImplementedError(f"Cell attribute {attr} not yet implemented")

                if cell_style:
                    cell_style = f' style="{cell_style[:-1]}"'

                if cell.is_header:
                    tag = "th"
                else:
                    tag = "td"

                content += f"<{tag}{cell_style}{cell_extra}>\n"
                content += cell.value
                content += f"</{tag}>\n"
            content += "</tr>\n"

        content += "</tbody>\n</table>\n"
        table.string = content
