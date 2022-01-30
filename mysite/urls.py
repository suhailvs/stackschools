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

from schools.models import School

class CustomDateSitemap(GenericSitemap):
    def lastmod(self, item):
        return timezone.datetime(2021, 12, 20, 20, 28, 1, tzinfo=timezone.utc)


my_sitemaps = {
    'schools': CustomDateSitemap({'queryset': School.objects.order_by('id'),'date_field': None}),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schools.urls')),

    path('sitemap.xml', sitemaps_views.index, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

]
