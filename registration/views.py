
def register(request):
    return render_to_response('need_to_activate')

def activate(request):
    return render_to_response('complete_profile')

