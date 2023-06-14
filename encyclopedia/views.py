from django.shortcuts import render

from . import util

import markdown2

import os
import fnmatch


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


def search(request):
    query = request.GET.get('q')
    if query:
        directory = 'entries/'
        results = []

        # Check if a file with the query name exists
        if os.path.isfile(os.path.join(directory, query + '.md')):
            title=query
            content = util.get_entry(title)
            html_content = markdown2.markdown(content)
            return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": html_content
            })

        # If not, perform a content search
        for filename in os.listdir(directory):
            if fnmatch.fnmatch(filename.lower(), '*{}*.md'.format(query.lower())):
                results.append(filename.replace('.md', ''))
        if results:
            return render(request, 'encyclopedia/search_results.html', {
                'query': query,
                'results': results})
        else:
            return render(request, 'encyclopedia/no_results.html', {'query': query})
    
    else:
        # Handle the case where query is an empty string
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })


def new_entry(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        directory = 'entries/'

        if os.path.isfile(os.path.join(directory, title + '.md')):
            return render(request, 'encyclopedia/error.html', {
                'message': 'There is already a page with this title.'
            })
        else:
            util.save_entry(title, content)
            html_content = markdown2.markdown(content)
            return render(request, "encyclopedia/page.html", {
                "title": title,
                "content": html_content
            })
    else:
        return render(request, "encyclopedia/new_entry.html")

