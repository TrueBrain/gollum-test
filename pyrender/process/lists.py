import wikitextparser

LIST_TYPES = {
    ";": ("dl", "dt"),
    ":": ("dl", "dd"),
    "*": ("ul", "li"),
    "#": ("ol", "li"),
}


def get_list_item_tag(list_type):
    if list_type not in LIST_TYPES:
        raise NotImplementedError(f"List type {list_type} not yet implemented")

    return LIST_TYPES[list_type]


def process_list(list: wikitextparser.WikiList):
    # We skipped a level; add the missing level (wikitextparser will reload
    # the node for us).
    if list.items[0] and list.items[0][0] in LIST_TYPES:
        list.string = f"{list.fullitems[0][list.level - 1] * list.level} \n{list.string}"

    current_list_tag = None
    content = ""

    for i in range(len(list.items)):
        # Soecial case for definition lists. Here you can have:
        # :;Item:Definition
        # This results in an unbalanced list, where one item is a level 2, and
        # the next item is a level 1.
        # This only happens if:
        # - This is not the first item
        # - This is level 2 or higher
        # - There isn't a list marker on the expected position
        # - The item before us indicates it is a definition list (;)
        # - We start with definition marker (:)
        if (
            i > 0
            and list.level > 1
            and (len(list.fullitems[i]) < 2 or list.fullitems[i][list.level - 1] not in LIST_TYPES)
            and list.fullitems[i - 1][list.level - 1] == ";"
            and list.fullitems[i][0] == ":"
        ):
            list_tag, item_tag = get_list_item_tag(":")
        else:
            list_tag, item_tag = get_list_item_tag(list.fullitems[i][list.level - 1])

        if current_list_tag != list_tag:
            if current_list_tag:
                content += f"</{current_list_tag}>"
            content += f"<{list_tag}>"
            current_list_tag = list_tag

        item = list.items[i].strip()
        content += f"<{item_tag}>"
        if item:
            content += f"{item}\n"

        for sublist in list.sublists(i):
            content += process_list(sublist)

        content += f"</{item_tag}>"

    content += f"</{current_list_tag}>\n"
    return content


def process_lists(wikitext: wikitextparser.WikiText):
    for list in reversed(wikitext.get_lists()):
        list.string = process_list(list)
