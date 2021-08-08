from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import CreateForm, SearchForm
from markdown2 import Markdown
import random, re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def detail(request, title):
    entry = util.get_entry(title)
    parser = Markdown()
    if entry is None:
        return redirect(reverse_lazy('error_page'))
    return render(request, "encyclopedia/title.html", {"entry": parser.convert(entry)})


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


def random_page(request, title):
    # entries = util.list_entries()
    # entry = util.get_entry(random.choice(entries))
    # return render(request, "encyclopedia/layout.html", {'entry': entry})
    pass


def error_404(request):
    return render(request, "encyclopedia/error.html")


def parser(mdText):
    htmlText = re.sub(r'^# (.*$)', r"<h1>\1</h1>", mdText, flags=re.I | re.M)
    htmlText2 = re.sub(r'## (.*$)', r"<h2>\1</h2>", htmlText, flags=re.M | re.I)
    htmlText3 = re.sub(r'^### (.*$)', r"<h3>\1</h3>", htmlText2, flags=re.M | re.I)
    htmlText4 = re.sub(r'\*\*(.*)\*\*', r"<b>\1</b>", htmlText3, flags=re.M | re.I)
    htmlText5 = re.sub(r'\*(.*)\*', r"<i>\1</i>", htmlText4, flags=re.M | re.I)
    htmlText6 = re.sub(r'\~\~(.*)\~\~', r"<del>\1</del>", htmlText5, flags=re.M | re.I)
    htmlText7 = re.sub(r'^\> (.*)', r"<blockquote>\1</blockquote>", htmlText6, flags=re.M | re.I)
    htmlText8 = re.sub(r'!\[(.*?)\]\((.*?)\)', r"<img alt='\1' src='\2' />", htmlText7, flags=re.M | re.I)
    htmlText9 = re.sub(r'\[(.*?)\]\((.*?)\)', r"<a href='\2'>\1</a>", htmlText8, flags=re.M | re.I)
    htmlText10 = re.sub(r'^\*|\- (.*?)', r"<li>\1</li>", htmlText9, flags=re.M | re.I)

    return htmlText10

