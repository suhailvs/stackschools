from rest_framework_gis.serializers import GeoFeatureModelSerializer
from schools.models import KeralaSchool

class MarkerSerializer(GeoFeatureModelSerializer):
    class Meta:
        fields = ("name","mal_address")
        geo_field = "GEOMETRY2"
        model = KeralaSchool