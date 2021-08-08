from django import forms


class CreateForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")


class SearchForm(forms.Form):
    search = forms.CharField(label="search")
