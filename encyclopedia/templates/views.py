from django.shortcuts import render

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/404.html', {'message': 'The requested page was not found.'})
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": html_content
    })