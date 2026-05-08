from datetime import datetime, timezone
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.auth import views as auth_views
from schools.views import home
from schools.models import School, KeralaSchool
from bachelorsportal.models import BPCollege
from postalcodes.models import PostalCode
class CustomDateSitemap(GenericSitemap):
    limit = 2000
    def lastmod(self, item):
        return datetime(2021, 12, 20, 20, 28, 1, tzinfo=timezone.utc)

my_sitemaps = {
    'schools': CustomDateSitemap({'queryset': School.objects.order_by('id'),'date_field': None}),
    'kerala_schools': CustomDateSitemap({ 'queryset': KeralaSchool.objects.order_by('id'),'date_field': None}),
    'colleges': CustomDateSitemap({ 'queryset': BPCollege.objects.order_by('id'),'date_field': None}),
    'postalcodes': CustomDateSitemap({ 'queryset': PostalCode.objects.order_by('id'),'date_field': None}),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('schools/', include('schools.urls')),
    path('postalcodes/', include('postalcodes.urls')),
    path('bp/', include('bachelorsportal.urls')),


    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    # path('accounts/signup/', signup, name='signup'),

    path('sitemap.xml', sitemaps_views.index, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

]
