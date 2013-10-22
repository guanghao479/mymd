from tastypie.resources import ModelResource
from django.contrib.auth.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'first_name', 'last_name', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'last_login']
        allowed_methods = ['get']