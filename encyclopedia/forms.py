from django import forms


class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.TextInput()
