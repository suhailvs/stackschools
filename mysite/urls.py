"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.utils import timezone
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from schools.views import home
from schools.models import School, KeralaSchool
from bachelorsportal.models import BPCollege
from postalcodes.models import PostalCode

class CustomDateSitemap(GenericSitemap):
    def lastmod(self, item):
        return timezone.datetime(2021, 12, 20, 20, 28, 1, tzinfo=timezone.utc)
class CustomDateSitemap2(GenericSitemap):
    def lastmod(self, item):
        return timezone.datetime(2025, 1, 22, 20, 28, 1, tzinfo=timezone.utc)


my_sitemaps = {
    'schools': CustomDateSitemap({'queryset': School.objects.order_by('id'),'date_field': None}),
    'kerala_schools': CustomDateSitemap({ 'queryset': KeralaSchool.objects.order_by('id'),'date_field': None}),
    'colleges': CustomDateSitemap2({ 'queryset': BPCollege.objects.order_by('id'),'date_field': None}),
    'postalcodes': CustomDateSitemap2({ 'queryset': PostalCode.objects.order_by('id'),'date_field': None}),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('schools/', include('schools.urls')),
    path('postalcodes/', include('postalcodes.urls')),
    path('bp/', include('bachelorsportal.urls')),
    path('map/', include('map.urls')),


    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    # path('accounts/signup/', signup, name='signup'),

    path('sitemap.xml', sitemaps_views.index, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

]
