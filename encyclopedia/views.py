from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import CreateForm, SearchForm
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def detail(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return redirect(reverse_lazy('error_page'))
    return render(request, "encyclopedia/title.html", {"entry": entry})


def create(request):
    if request.method == 'POST':

        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
        return redirect('/')
    else:
        return render(request, 'encyclopedia/create.html', {'form': CreateForm()})


def edit(request):
    pass


def search_result(request):
    entries = util.list_entries()
    results = []
    if request.method == 'GET':
        search = request.GET.get('search')
        for entry in entries:
            if entry.lower().__contains__(search.lower()):
                results += entry
        return render(request, "encyclopedia/search.html", {"results": results})
    else:
        return render(request, "encyclopedia/layout.html", {"form": SearchForm()})


def random_page(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return render(request, "encyclopedia/layout.html", {'entry': entry})


def error_404(request):
    return render(request, "encyclopedia/error.html")
