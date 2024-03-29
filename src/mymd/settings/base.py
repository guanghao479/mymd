# Django settings for mymd project.
from unipath import Path
from django.core.urlresolvers import reverse

PROJECT_ROOT = Path(__file__).ancestor(3)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT.child("media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "http://127.0.0.1:8000/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT.child("static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_ROOT.child("static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# TODO: This should not be in repository, should be in environment virables
#       Refer to "Two Scoop of Django for 1.5 - 5.5"
SECRET_KEY = 'q^4doyj_$30ncqru*&amp;h1c0!qd%_#bfrw_-z7a7pu1v7+d*&amp;==t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT.child("templates"),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mymd.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mymd.wsgi.application'


# Order is important!!! maintain the home brewed apps on top will make
# them higher priority
INSTALLED_APPS = (
    # home brewed apps !!!! Please follow A->Z
    "about",
    "account",
    "actstream",
    "avatar",
    "city",
    "community",
    "diary",
    "district",
    "disease",
    "experiences",
    "friends",
    "home",
    "meetup",
    "mymdutils",
    "profiles",
    "stream",

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    "django_forms_bootstrap",
    "emailconfirmation",
    "haystack",
    "notification", # must be first
    "pagination",
    "pinax_theme_bootstrap",
    "redactor",
    "social_auth",
    "south",
    "taggit",
    "taggit_templatetags",
    "tastypie",
    'widget_tweaks',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


##############################################################################
# Project specific settings

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "account.context_processors.account",
    "notification.context_processors.notification",
    "mymdutils.context_processors.search",
]

#Django Authentication Backends
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.contrib.douban.DoubanBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.skyrock.SkyrockBackend',
    'social_auth.backends.contrib.flickr.FlickrBackend',
    'social_auth.backends.contrib.instagram.InstagramBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.yandex.YandexBackend',
    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.OpenIDBackend',
    'social_auth.backends.contrib.live.LiveBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.douban.DoubanBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.vkontakte.VKontakteBackend',
    'social_auth.backends.contrib.yandex.YandexOAuth2Backend',
    'social_auth.backends.contrib.yandex.YaruBackend',
    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
    'social_auth.backends.contrib.vkontakte.VKontakteOAuth2Backend',
    'social_auth.backends.contrib.mailru.MailruBackend',
    'django.contrib.auth.backends.ModelBackend',
    'account.auth_backends.AuthenticationBackend',
)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse("profile:profile_detail", kwargs={"username":u.username}),
}

# Account Settings
#=================
AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = True
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "what_next"
LOGOUT_REDIRECT_URLNAME = "home"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

# Social Auth Settings
#=====================
#GOOGLE_CONSUMER_KEY = 'lktest.sinaapp.com'
#GOOGLE_CONSUMER_SECRET = 'Cq7ESWzLcmdTrRW7RZpor_Oo'
DOUBAN_CONSUMER_KEY = '094e0fa52914923c1bea2eef7b3db6b4'
DOUBAN_CONSUMER_SECRET = 'f090f610a931d71f'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/about/what_next'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/about/what_next'

# Activity Stream Settings
#=========================
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.User', 'experiences.Post'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': False,
    'GFK_FETCH_DEPTH': 0,
}

#Haystack configuration
#======================
HAYSTACK_CONNECTIONS = {
    'default':{
        'ENGINE':'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
        },
}

# Pagination settings
#====================
PAGINATE_NUM = 10

# Meetup settings
#================
MEETUP_POSTER_STORAGE_DIR = 'static/images/meetup/posters/'

# Redactor settings
#================
REDACTOR_SETTINGS = {
    'autoformat': True,
    'lang': 'zh_cn',
    'overlay': True,
    }
