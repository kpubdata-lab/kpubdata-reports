"""두 문서 생성 스크립트가 함께 쓰는 HTML 조각 함수."""


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def table(head, rows, cls="", widths=None):
    ths = ""
    for i, h in enumerate(head):
        w = f' style="width:{widths[i]}"' if widths and widths[i] else ""
        ths += f"<th{w}>{h}</th>"
    body = ""
    for r in rows:
        body += "<tr>" + "".join(x if x.startswith("<td") else f"<td>{x}</td>" for x in r) + "</tr>"
    return f'<div class="tablewrap"><table class="{cls}"><tr>{ths}</tr>{body}</table></div>'


def c(text, rowspan=None):
    rs = f' rowspan="{rowspan}"' if rowspan else ""
    return f'<td class="c"{rs}>{text}</td>'


def fig(name, alt, cls=""):
    return f'<div class="figure {cls}"><img src="figures/{name}" alt="{alt}"></div>'


def sheet(title, body, brk=True):
    b = " break" if brk else ""
    return f'<section class="sheet{b}">\n<h2 class="bar">{title}</h2>\n{body}\n</section>\n'
