
from django.shortcuts import render
from bachelorsportal.views import incr_counter

from schools.models import KeralaSchool


from rest_framework import viewsets
from rest_framework_gis import filters

from map.serializers import MarkerSerializer


class MarkerViewSet(viewsets.ReadOnlyModelViewSet):
    bbox_filter_field = "GEOMETRY"
    filter_backends = (filters.InBBoxFilter,)
    queryset = KeralaSchool.objects.all()
    serializer_class = MarkerSerializer

def home(request):
    # kerala school
    incr_counter('map')
    return render(request,'map/home.html')
