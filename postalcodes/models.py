from django.contrib.gis.db import models
from django.urls import reverse
# Create your models here.
class PostalCode(models.Model):
    country = models.CharField(max_length=2,db_index=True)
    postal_code = models.CharField(max_length=20,db_index=True)
    place = models.CharField(max_length=180)
    admin_name1= models.CharField(max_length=100) # state
    admin_code1= models.CharField(max_length=20)

    admin_name2= models.CharField(max_length=100) # county/province
    admin_code2= models.CharField(max_length=20)

    admin_name3= models.CharField(max_length=100) # community
    admin_code3= models.CharField(max_length=20)

    lat = models.CharField(max_length=30, blank=True)
    lon = models.CharField(max_length=30, blank=True)
    accuracy = models.SmallIntegerField() # accuracy of lat/lng from 1=estimated, 4=geonameid, 6=centroid of addresses or shape
    GEOMETRY = models.PointField(null=True)

    def get_absolute_url(self):        
        return reverse('postalcodes:postalcode_view', kwargs={'code' : self.postal_code})
        