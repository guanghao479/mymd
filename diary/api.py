from tastypie.resources import ModelResource
from tastypie import fields
from diary.models import Diary
from mymd.api import UserResource
from tastypie.authentication import SessionAuthentication

class DiaryResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)

    class Meta:
        queryset = Diary.objects.all()
        resource_name = 'diary'
        authentication = SessionAuthentication()

