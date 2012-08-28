from django.http import HttpResponse
from django.utils.encoding import smart_unicode
from django.utils import simplejson as json

from district.models import District

class JSONResponse(HttpResponse):
    def __init__(self, data):
        super(JSONResponse, self).__init__(
                json.dumps(data), mimetype='application/json')

def city_for_district(request):
    result = {}
    if request.is_ajax() and request.GET and 'district_id' in request.GET:
        obj = District.objects.get(id=request.GET['district_id']);
        city = obj.city
        result={"city": {"city_id": city.id}}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return JSONResponse({'error': 'Not Ajax or no GET'})
