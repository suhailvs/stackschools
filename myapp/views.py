from django.views.generic.base import TemplateView

from schools.models import KeralaSchool


from rest_framework import viewsets
from rest_framework_gis import filters

from myapp.serializers import MarkerSerializer


class MarkerViewSet(viewsets.ReadOnlyModelViewSet):
    bbox_filter_field = "GEOMETRY"
    filter_backends = (filters.InBBoxFilter,)
    queryset = KeralaSchool.objects.all()
    serializer_class = MarkerSerializer

class MarkersMapView(TemplateView):
    template_name = "map.html"
