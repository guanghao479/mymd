from django.shortcuts import render_to_response
from django.shortcuts import redirect

from registration.forms import RegistrationForm
from registration.models import RegistrationActivation as RegManager

from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_
from django.contrib.auth import logout as logout_
from django.contrib.auth.forms import AuthenticationForm

from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_protect
def register(request, template_name='registration/registration_form.html'):
    """
    Register user view. Using registration form to valid data. If success,
    redirect to needs activation page. Otherwise generate registration page
    with error message.

    """
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            RegManager.objects.register(request, **form.cleaned_data)
            return HttpResponseRedirect('/register/needs_activation/')
    else:
        form = RegistrationForm()

    c['form'] = form
    return render_to_response('registration/register.html',
                              RequestContext(request, c))

def needs_activation(request):
    """
    View for need activation page.

    """
    return render_to_response('registration/needs_activation.html',
                              RequestContext(request, {}))

def activate(request, activation_key):
    """
    Activate user using activation key. If success, redirect to login
    Page. Otherwise redirect to activation error page.

    """
    user = RegManager.objects.activate_user(request, activation_key)
    if user:
        path = '/user/{0}'.format(user.username)
        return redirect(path)
    return redirect('/')

@csrf_protect
def login(request):
    """
    Login user using Django build-in login and authentication method.
    If user authentication success, redirect to home page. Otherwise
    Generate login page with error message.

    """
    #If user already login, we just render home page.
    if request.user.is_authenticated():
        return render_to_response('home/home.html', RequestContext(request,{}))

    #Otherwise we check login user in.
    if request.POST:
        login_user = authenticate(username=request.POST['username'],
                                  password=request.POST['password'])
        if login_user is not None:
            login_(request, login_user)
            return redirect('/')
        else:
            #set test cookie to see if user enable cookie in their browser.
            form = AuthenticationForm(request)
            request.session.set_test_cookie()
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()

    context = csrf(request)
    context.update({
        'form': form,
        'request': request})
    return render_to_response('registration/login.html', RequestContext(request, context))

@csrf_protect
def logout(request):
    """
    Log out user. If succeed. redirect to index page.

    """
    logout_(request)
    return redirect(reverse('login'))
