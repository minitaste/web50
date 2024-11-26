import markdown
from random import choice 
from django.shortcuts import render, redirect


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content,
        })
    return redirect("index")

def search(request):
    query = request.GET.get('q', '')  
    if query:
        entries = util.list_entries()
        search_results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "search_results": search_results,
        })
    else:
        return redirect("index")

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            util.save_entry(title, content)
            return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    content = util.get_entry(title)
    if not content:
        return redirect("index")
    if request.method == "POST":
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')

        if new_title or new_content:
            util.save_entry(new_title, new_content)
            return redirect("entry", title=new_title)
        
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
    })

def random(request):
    entries = util.list_entries()
    if not entries:
        return redirect("index")
    page_name = choice(entries)
    return redirect("entry", title=page_name)
