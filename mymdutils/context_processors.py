from django.conf import settings
from haystack.forms import SearchForm

def search(request):
    return {
        "nav_search_form": SearchForm(load_all=True),
    }
