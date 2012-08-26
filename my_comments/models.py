from django.db import models
from django.contrib.comments.models import Comment

class MyComment(Comment):
    """
    We do not want user_name, user_email and user_url,
    Because these field are in user object.
    """
