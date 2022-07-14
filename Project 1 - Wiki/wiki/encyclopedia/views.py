from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from markdown2 import Markdown
import markdown2

from . import util
from .forms import EditPageForm, NewPageForm
import random


def index(request):
    """_summary_
        Displays all encyclopedia entries from disk.
        
        steps:
        Gets all entries from list_entries() function of util.py and renders the index.html page which displays the entries list

    """
    entries=util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries})
    
def entry(request, title):   
    """
        Renders the content of an encylopedia entry selected by a user
        
        1. Gets the content of the selected encyclopedia entry by checking that the entry exists
        2. Renders the HTML content of the entry if exists else renders an error page to the user 
    """ 
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/entry.html", 
                  {"title": title, "content": markdown2.markdown(content)})
    
def search(request):
    """
        Allows user to type a query into the search box to search for an encyclopedia entry
        
        1. Get the search query
        2. Redirect the user to the entry page searched if the query matches an encyclopedia entry
        3. If query doesn't match, display a list of entries that have the query as a susbstring
    """
    if request.method == "POST":
        title = request.POST.get('q')
        entries = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
        # Checks if entry title matches an entry in the list
        if title in util.list_entries():
            return HttpResponseRedirect(reverse("wiki:entry", args=[title]))
        else:
            # renders error page if the search result finds no match
            if len(entries) == 0:
                return entry(request, title)
            # renders the search result list of entries with query as susbstring
            else:
                return render(request, "encyclopedia/search_result.html", {"entries": entries})

def create(request):
    """
        Allows user to create a new encyclopedia entry
        
        1. Get page title and body from NewPageForm
        2. Displays errror message if the page title exists
        3. if new page, save the title and its contents and redirects user to the entry
    """
    
    form = NewPageForm(request.POST or None)
    context = {}
    context['form'] = form
    if request.POST:
        if form.is_valid():
            title = form.clean_title()
            content = form.clean_content()
            if title in util.list_entries():
                messages.error(request, f"Page already exists with the title {title}.\n Please try with a different title!")
                return HttpResponseRedirect(reverse("wiki:create"))
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=[title]))
    return render(request, "encyclopedia/create_page.html",context)

def edit(request, title):
    """
        Allows user to edit an entry's Markdown content with the entry pre-poulated with its initial content
        
        1. Get the page name from form and content
        2. Create an edit form object with initial content
        3. Render to edit_page html with pre-populated information
    """
    con = util.get_entry(title)
    form = EditPageForm(request.POST or None, initial = {'content':con})
    context = {'title':title} 
    context['form'] = form
    if request.POST:
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=[title]))
    return render(request, "encyclopedia/edit.html", context)
    
def random_page(request):
    """
        Takes user to a random encyclopedia entry 
    """
    random_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:entry", args=[random_title]))
    
