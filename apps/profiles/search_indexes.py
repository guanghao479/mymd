#from haystack import indexes
#from profiles.models import Profile
#
#class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
#    city = indexes.CharField(model_attr='city')
#
#    def get_model(self):
#        return Profile