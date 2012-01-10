from django.shortcuts import render_to_response
from django.shortcuts import redirect
from registration.forms import RegistrationForm
from registration.models import RegistrationActivation as RegManager
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect

def register(request, template_name='registration/registration_form.html'):
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
    return render_to_response('registration/register.html', RequestContext(request, c))

def needs_activation(request):
    return render_to_response('registration/needs_activation.html', RequestContext(request, {}))

def activate(request, activation_key):
    user = RegManager.objects.activate_user(request, activation_key)
    if user:
        path = '/user/{0}'.format(user.username)
        return redirect(path)
    return redirect('/')