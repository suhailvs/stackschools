from django.http import HttpResponseBadRequest, HttpResponseRedirect
from functools import wraps

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if is_ajax(request=request):
            return f(request, *args, **kwargs)
        return HttpResponseBadRequest()
        
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap