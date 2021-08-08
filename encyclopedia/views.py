from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def detail(request, title):

    try:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/title.html", {"entry": entry})
    except FileNotFoundError:
        return redirect(reverse_lazy('error_page'))


def error_404(request, title):
    return render(request, "encyclopedia/error.html", {'title': title})
