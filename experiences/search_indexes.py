import datetime
from haystack import indexes
from experiences.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    body = indexes.CharField(model_attr='body')
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Post