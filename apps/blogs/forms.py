from django.contrib.auth.models import User
from django import forms
from blogs.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'allow_comments')
