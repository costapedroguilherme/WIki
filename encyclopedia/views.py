from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    return render(request, "encyclopedia/wiki.html", {
        "content": markdown2.markdown(util.get_entry(name))
    })
