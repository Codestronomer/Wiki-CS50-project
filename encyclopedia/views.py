from django.shortcuts import render, redirect
from .forms import CreateForm, SearchForm, EditForm
from django.views.generic import ListView
from django.urls import reverse_lazy
from markdown2 import Markdown
from . import util
import random


# List available entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Renders Entries in Detail
def detail(request, title):
    entry = util.get_entry(title)
    name = title
    parser = Markdown()
    if entry is None:
        return redirect(reverse_lazy('error_page'))
    return render(request, "encyclopedia/title.html", {"entry": parser.convert(entry), "name": title})


# Create and save entries
def create(request):
    entries = util.list_entries()
    if request.method == 'POST':

        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            for entry in entries:
                if title.lower() == entry.lower():
                    return redirect(reverse_lazy("error_page"))
                else:
                    util.save_entry(title, content)
        return redirect('/')
    else:
        return render(request, 'encyclopedia/create.html', {'form': CreateForm()})


# Edits and saves entries
def edit(request, title):
    name = title
    entry = util.get_entry(title)
    if entry is None:
        return redirect(reverse_lazy('error_page'))
    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect("/")
    else:
        return render(request, "encyclopedia/edit.html", {'content': entry, "name": name})


# Returns search result from queries
def search_result(request):
    entries = util.list_entries()
    results = []
    if request.method == 'GET':
        search = request.GET.get('search')
        for entry in entries:
            if search.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {"results": results})
    else:
        return render(request, "encyclopedia/layout.html", {"form": SearchForm()})


# Renders a random entry page
def random_page(request):
    parser = Markdown()
    entries = util.list_entries()
    entry = random.choice(entries)
    rand_entry = util.get_entry(entry)
    return render(request, "encyclopedia/title.html", {'entry': parser.convert(rand_entry), 'name': entry})


# Renders Error page
def error_404(request):
    return render(request, "encyclopedia/error.html")