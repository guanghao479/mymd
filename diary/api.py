from tastypie.resources import ModelResource
from tastypie import fields
from diary.models import Diary
from mymd.api import UserResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from django.core.urlresolvers import reverse

class DiaryResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)

    class Meta:
        queryset = Diary.objects.all()
        resource_name = 'diary'
        authentication = SessionAuthentication()
        authorization = Authorization()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(author=request.user)

    def dehydrate_modified_date(self, bundle):
        return bundle.obj.modified_date.strftime("%A %d %B %Y %I:%M%p")

    def dehydrate(self, bundle):
        bundle.data['uri'] = reverse('diary_detail', kwargs={'id':bundle.obj.id})
        return bundle
