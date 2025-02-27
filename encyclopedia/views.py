from django.shortcuts import render
import markdown2
from django import forms

from . import util

class NewTaskForm(forms.Form):
    search = forms.CharField(label='')
    search.widget.attrs.update({'class': 'search', 'placeholder': 'Search Encyclopedia', 'name': 'q'})

def index(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if util.get_entry(search):
                return render(request, "encyclopedia/wiki.html", {
                    "form": NewTaskForm(),
                    "content": markdown2.markdown(util.get_entry(search)) 
                })
            else:
                if util.search_entry(search):
                    return render(request, "encyclopedia/search.html", {
                        "form": NewTaskForm(),
                        "title": search.capitalize(),
                        "entries": util.search_entry(search)
                    })
                else:
                    return render(request, "encyclopedia/wiki.html", {
                        "form": NewTaskForm(),
                        "content": f"<h1>{search.capitalize()}</h1><p>No result found for this search.</p>"
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form,
                "entries": util.list_entries()
            })
    return render(request, "encyclopedia/index.html", {
        "form": NewTaskForm(),
        "entries": util.list_entries()
    })

def wiki(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/wiki.html", {
            "form": NewTaskForm(),
            "content": markdown2.markdown(content) 
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "form": NewTaskForm(),
            "content": f"<h1>{title.capitalize()}</h1><p>Encyclopedia does not have an article with this exact name.</p>"
        })