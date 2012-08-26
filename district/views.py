from django.http import HttpResponse
from django.utils.encoding import smart_unicode
from django.utils import simplejson as json

from district.models import District

class JSONResponse(HttpResponse):
    def __init__(self, data):
        super(JSONResponse, self).__init__(
                json.dumps(data), mimetype='application/json')

def district_for_city(request):
    result = {}
    if request.is_ajax() and request.GET and 'city_id' in request.GET:
        objs = District.objects.filter(city=request.GET['city_id'])
        district_list = []
        for district in objs:
            district_content = {}
            district_content['id'] = district.id
            district_content['name'] = district.name
            district_list.append(district_content)
        result['districts'] = district_list
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return JSONResponse({'error': 'Not Ajax or no GET'})