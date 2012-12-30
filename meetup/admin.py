from django.contrib import admin
from meetup.models import Meetup, AttendManager, Attend

admin.site.register(Meetup)
admin.site.register(AttendManager)
admin.site.register(Attend)
