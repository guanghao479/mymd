from functools import wraps
from django.utils.decorators import available_attrs
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render_to_response
from django.template import RequestContext

'''
TODO: move this to a global util app
'''
def ownership_required(get_owner_func, login_url='/accounts/login/', redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                path = request.build_absolute_uri()
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                            settings.LOGIN_URL)[:2]
                current_scheme, current_netloc = urlparse.urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(path, login_url, redirect_field_name)
            elif not request.user == get_owner_func(request, *args, **kwargs):
                resp = render_to_response('403.html', context_instance=RequestContext(request))
                resp.status_code = 403
                return resp
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator