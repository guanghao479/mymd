from django.conf import settings

MEETUP_POSTER_STORAGE_DIR = getattr(settings, 'MEETUP_POSTER_STORAGE_DIR', 'poster')