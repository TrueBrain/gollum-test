def render_html(category, language, page, body):
    content = "<html><head>\n"
    content += '<meta http-equiv="Content-type" content="text/html;charset=utf-8">\n'
    content += '<link rel="stylesheet" type="text/css" href="/gollum.css" media="all">\n'
    content += f"<title>OpenTTD - {page}</title>"
    content += (
        '</head><body class="webkit">\n<div class="container-lg clearfix">\n<div id="wiki-wrapper" class="page">\n'
    )
    content += f'<div id="wiki-content"><h1 class="pt-4">{page}</h1>\n'
    content += '<div id="wiki-body" class="gollum-mediawiki-content overflow-hidden "><div class="markdown-body">'
    content += body
    content += "</body>\n"

    return content


def write_html(category, language, page, body):
    with open("data/result.html", "w") as f:
        f.write(render_html(category, language, page, body))
