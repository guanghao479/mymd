from tastypie.resources import ModelResource
from diary.models import Diary

class DiaryResource(ModelResource):
    class Meta:
        queryset = Diary.objects.all()
        resource_name = 'diary'