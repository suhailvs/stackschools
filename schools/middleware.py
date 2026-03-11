# middleware.py
from django.http import HttpResponseForbidden
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

BLOCKED_COUNTRIES = ['CN', 'SG']

class GeoBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        country = request.META.get('HTTP_CF_IPCOUNTRY')
        if country in BLOCKED_COUNTRIES:
            return HttpResponseForbidden("Access denied")
        return self.get_response(request)

class SabbathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "IS_SABBATH", True):
            html = render_to_string("sabbath.html")
            return HttpResponse(html, status=503)
        response = self.get_response(request)
        return response