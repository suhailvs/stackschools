from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.
class BPCollege(models.Model):
    code = models.IntegerField(unique=True,db_index=True)
    title  = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    summary = models.TextField()
    fee_int = models.IntegerField(null=True)
    fee_int_currency = models.CharField(max_length=20)
    fee_nat = models.IntegerField(null=True)
    fee_nat_currency = models.CharField(max_length=20)
    duration = models.SmallIntegerField(null=True)
    university = models.CharField(max_length=200)
    university_logo = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    fullonline = models.BooleanField(null=True)
    online = models.BooleanField(null=True)
    oncampus = models.BooleanField(null=True)
    fulltime = models.BooleanField(null=True)
    parttime = models.BooleanField(null=True)
    ielts = models.SmallIntegerField(null=True)
    toefl = models.SmallIntegerField(null=True)

    def get_absolute_url(self):        
        url = reverse('bachelorsportal:college_view', kwargs={'code' : self.code})
        return f"{url}{slugify(self.title)[:50]}-{slugify(self.university)[:30]}-{slugify(self.city)}"

