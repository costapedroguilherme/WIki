import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def new_entry(title, content):
    """
    Saves an new encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    a error is displayed.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return False
    default_storage.save(filename, ContentFile(f"#{title}\n".encode("utf-8") + content.encode("utf-8")))
    return True

def save_entry(title, content):
    """
    Replaces a entry with a version with its new content.
    """
    filename = f"entries/{title}.md"
    default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def search_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, search for similar results to be displayed in
    a list.
    """
    return list(entry for entry in list_entries() if title.lower() in entry.lower())

def get_random():
    """
    Retrieves a random page from the encyclopedia.
    """
    return random.choice(list_entries())