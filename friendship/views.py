from django.http import HttpResponse
from django.core import serializers
from friendship.models import Friendship

def accept(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == 'POST':
            mimetype = 'application/javascript'
            data = serializers.serialize('json', Friendship.objects.all())
            return HttpResponse(data,mimetype)
    return HttpResponse(status=400)
        

def invite(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == 'POST':
            mimetype = 'application/javascript'
            data = serializers.serialize('json', Friendship.objects.all())
            return HttpResponse(data,mimetype)
    return HttpResponse(status=400)