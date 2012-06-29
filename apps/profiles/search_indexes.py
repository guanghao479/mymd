from haystack.indexes import *
from haystack import site
#from profile.models import Profile

class ProfileIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    city = CharField(model_attr='city')
    disease = CharField(model_attr='disease')
