from tastypie.resources import ModelResource
from experiences.models import Post

class ExperienceResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'experience'