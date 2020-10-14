import html
import wikitextparser


def process_tables(wikitext: wikitextparser.WikiText):
    for table in reversed(wikitext.get_tables()):
        process_tables(table)

        table_style = ""
        table_extra = ""
        for attr in table.attrs:
            if attr == "style":
                style = html.escape(table.attrs["style"], quote=False).replace('"', "'").strip()
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
                table_extra += f' {attr}="{html.escape(table.attrs[attr]).strip()}"'
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

                for attr in cell.attrs:
                    if attr == "colspan":
                        cell_extra += f' colspan="{cell.attrs["colspan"]}"'
                        skip_cells = int(cell.attrs["colspan"]) - 1
                    elif attr == "rowspan":
                        cell_extra += f' rowspan="{cell.attrs["rowspan"]}"'
                        # TODO -- What to skip?
                        # skip_cells = int(cell.attrs["colspan"]) - 1
                    elif attr == "style":
                        style = html.escape(cell.attrs["style"], quote=False).replace('"', "'").strip()
                        if style[-1] != ";":
                            style += ";"
                        cell_style += f"{style} "
                    elif attr in ("align", "bgcolor", "class", "height", "scope", "valign", "width"):
                        cell_extra += f' {attr}="{html.escape(cell.attrs[attr]).strip()}"'
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
