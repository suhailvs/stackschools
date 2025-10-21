# middleware.py
from django.http import HttpResponseForbidden

BLOCKED_COUNTRIES = ['CN', 'SG']

class GeoBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        country = request.META.get('CF_IPCOUNTRY')
        if country in BLOCKED_COUNTRIES:
            return HttpResponseForbidden("Access denied")
        return self.get_response(request)
