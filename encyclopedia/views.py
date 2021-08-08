from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CreateForm

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
            form.save()
        return redirect('/')
    else:
        return render(request, 'encyclopedia/create.html', {'form': CreateForm()})


def error_404(request):
    return render(request, "encyclopedia/error.html")
