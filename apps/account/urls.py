from django.conf import settings
from django.conf.urls.defaults import patterns, url
from social_auth.views import auth, complete, disconnect


#if settings.ACCOUNT_OPEN_SIGNUP:
#    signup_view = "account.views.signup"
#else:
#    signup_view = "pinax.apps.signup_codes.views.signup"


urlpatterns = patterns("",
    url(r"^email/$", "account.views.email", name="acct_email"),
    url(r"^signup/$", "account.views.signup", name="acct_signup"),
    url(r"^login/$", "account.views.login", name="acct_login"),
    url(r'^login/(?P<backend>[^/]+)/$', auth, name='socialauth_begin'),
    url(r'^login/complete/(?P<backend>[^/]+)/$', complete, name='socialauth_complete'),
    url(r"^login/openid/$", "account.views.login", {"associate_openid": True}, name="acct_login_openid"),
    url(r"^password_change/$", "account.views.password_change", name="acct_passwd"),
    url(r"^password_set/$", "account.views.password_set", name="acct_passwd_set"),
    url(r"^password_delete/$", "account.views.password_delete", name="acct_passwd_delete"),
    url(r"^password_delete/done/$", "django.views.generic.simple.direct_to_template", {"template": "account/password_delete_done.html"}, name="acct_passwd_delete_done"),
    url(r"^timezone/$", "account.views.timezone_change", name="acct_timezone_change"),
    url(r"^language/$", "account.views.language_change", name="acct_language_change"),
    url(r"^logout/$", "account.views.logout", {"template_name": "account/logout.html"}, name="acct_logout"),
    url(r"^confirm_email/(\w+)/$", "emailconfirmation.views.confirm_email", name="acct_confirm_email"),
    url(r"^password_reset/$", "account.views.password_reset", name="acct_passwd_reset"),
    url(r"^password_reset/done/$", "account.views.password_reset_done", name="acct_passwd_reset_done"),
    url(r"^password_reset_key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", "account.views.password_reset_from_key", name="acct_passwd_reset_key"),
)
