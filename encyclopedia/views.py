from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import CreateForm, SearchForm, EditForm
from markdown2 import Markdown
import random, re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def detail(request, title):
    entry = util.get_entry(title)
    name = title
    parser = Markdown()
    if entry is None:
        return redirect(reverse_lazy('error_page'))
    return render(request, "encyclopedia/title.html", {"entry": parser.convert(entry), "name": title})


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


def parsered(mdText):
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

