from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from markdownx.fields import MarkdownxFormField


class NoteForm(forms.Form):
    note_text = MarkdownxFormField(label='')
    note_text.widget.template_name = 'notes/markdownx_bootstrap.html'
    note_text.widget.attrs.update({'style': 'width: 100%', 'rows': 30})


def note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/')

    form = NoteForm()

    return render(request, 'notes/note_view.html', {'form': form})
