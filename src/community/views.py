from django.http import HttpResponse
from django.utils.encoding import smart_unicode
from django.utils import simplejson as json

from community.models import Community

class JSONResponse(HttpResponse):
    def __init__(self, data):
        super(JSONResponse, self).__init__(
                json.dumps(data), mimetype='application/json')

def community_for_district(request):
    result = {}
    if request.is_ajax() and request.GET and 'district_id' in request.GET:
        objs = Community.objects.filter(district=request.GET['district_id'])
        community_list = []
        for community in objs:
            community_content = {}
            community_content['id'] = community.id
            community_content['name'] = community.name
            community_list.append(community_content)
        result['communities'] = community_list
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return JSONResponse({'error': 'Not Ajax or no GET'})
