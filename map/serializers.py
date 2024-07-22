from rest_framework_gis.serializers import GeoFeatureModelSerializer
from schools.models import KeralaSchool

class MarkerSerializer(GeoFeatureModelSerializer):
    class Meta:
        fields = ("name","code")
        geo_field = "GEOMETRY"
        model = KeralaSchool