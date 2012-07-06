import datetime
from haystack import indexes
from blogs.models import Post


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Blog

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects