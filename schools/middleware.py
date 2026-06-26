# middleware.py
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
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

    def _in_sabbath_window(self,now):        
        weekday = now.weekday()  # Monday=0 ... Friday=4, Saturday=5
        hour = now.hour
        if weekday == 4 and hour >= 18:
            return True
        if weekday == 5 and hour < 18:
            return True
        return False
    
    def __call__(self, request):
        now = datetime.now(IST)
        if self._in_sabbath_window(now):            
            html = render_to_string("sabbath.html", {'now': now.strftime("%A %I:%M %p")})
            return HttpResponse(html, status=503)
        response = self.get_response(request)
        return response