from tastypie.resources import ModelResource
from tastypie import fields
from diary.models import Diary
from mymd.api import UserResource

class DiaryResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author')

    class Meta:
        queryset = Diary.objects.all()
        resource_name = 'diary'