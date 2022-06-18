from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.template.defaultfilters import slugify
from activities.models import Notification
# Create your models here.



class GeneralSettings(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.key}:{self.value}'


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    log_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


class School(models.Model):
    """
    school_category: {
        '10-Secondary with Higher Secondary': 2717,
        '11-Higher Secondary only/Jr. College': 10,
        '1-Primary': 68182,
        '2-Primary with Upper Primary': 25853,
        '3-Pr. with Up.Pr. Sec. and H.Sec.': 2062,
        '4-Upper Primary only': 15863,
        '5-Up. Pr. Secondary and Higher Sec': 3857,
        '6-Pr. Up Pr. and Secondary Only': 3927,
        '7-Upper Pr. and Secondary': 2048,
        '8-Secondary Only': 2192
    }
    school_type: {'1-Boys': 598, '2-Girls': 1987, 
        '3-Co-educational': 124126}
    

    {'101-Other Central Govt. Schools': 2, '17-KGBV': 295, '1-Department of Education': 24019, '1-Dept. Of education': 54438, 
        '2-Tribal Welfare Department': 225, '3-Local Body': 52, '4-Government Aided': 30, '4-Govt. aided': 3120, 
        '5-Private Unaided (Recognized)': 5697, '5-Pvt. Unaided (Recognized)': 32164, '6-Other Govt. Managed schools': 6, 
        '8-Unrecognized': 39, '90-Social Welfare Dept.': 27, '91-Ministry of Labour': 2, '92-Central School': 45, '92-Kendriya Vidyalaya': 39, 
        '93-Jawahar Navodaya Vidhyalaya': 42, '93-Jawahar Navodaya Vidyalaya': 19, '97-Madarsa recognized (by Wakf board/Madarsa Board)': 68, 
        '97-Madarsa Recognized (by Wakf board/Madarsa Board)': 5387, '98-Madarsa unrecognized': 5, '98-Madarsa Unrecognized': 990}
    state_management

    {'101-Other Central Govt Managed Schools': 2, '1-Department of Education': 78752, '2-Tribal Welfare Department': 225, '3-Local body': 52, 
        '4-Government Aided': 3150, '5-Private Unaided (Recognized)': 37861, '6-Other Govt. Managed Schools': 6, '8-Unrecognized': 39, 
        '90-Social welfare Department': 27, '91-Ministry of Labor': 2, '92-Kendriya Vidyalaya': 84, '93-Jawahar Navodaya Vidyalaya': 61, 
        '97-Madarsa recognized (by Wakf board/Madarsa Board)': 5455, '98-Madarsa unrecognized': 995}
    national_management

    {'': 26687, '1-Yes': 20989, '2-No': 79035}
    pre_primary

    {'10-School running in other Department Building': 161, '1-Private': 41820, '2-Rented': 7494, '3-Government': 73799, 
        '4-Government school in a rent free building': 2863, '5-No Building': 356, '7-Building Under Construction': 218}
    building_status

    {'1-Pucca': 74648, '2-Pucca but broken': 8648, '3-Barbed wire fencing': 1451, '4-Hedges': 696, '5-No boundary walls': 35335, 
        '6-Others': 1019, '7-Partial': 3625, '8-Under Construction': 1289}
    boundary_wall

    {'Yes': 126711}
    drinking_water_availability

    {'Yes': 126711}
    hand_wash_facility

    {'1-Yes': 67160, '2-No': 59551}
    library

    {'1-Yes': 22771, '2-No': 103940}
    reading_corner

    {'1-Yes': 56159, '2-No': 70552}
    book_bank

    {'1-Yes': 15332, '2-No': 111379}
    internet

    {'1-Yes': 4025, '2-No': 122686}
    dth

    """
    code = models.IntegerField(default=1000000) # 7 digit integer
    school_name = models.CharField(max_length=200)

    # 11 digit integer may starts with 0, first two digits representing the State 
    # and the following two digits representing the District.
    # select udise_code FROM "schools_school2" where (udise_code ~* '[a-z]') is true
    udise_code = models.CharField(max_length=11)

    # address
    state = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    block = models.CharField(max_length=60)
    cluster = models.CharField(max_length=200)
    village = models.CharField(max_length=60)
    pincode = models.CharField(max_length=6) # six digit pincode
    
    school_category = models.CharField(max_length=60)
    school_type = models.CharField(max_length=60)
    class_from = models.SmallIntegerField()
    class_to = models.SmallIntegerField()
    state_management = models.CharField(max_length=200) #5-Private Unaided (Recognized)
    national_management = models.CharField(max_length=200)
    status = models.CharField(max_length=60)
    location = models.CharField(max_length=60)
    aff_board_sec = models.CharField(max_length=60)
    aff_board_hsec = models.CharField(max_length=60)
    year_of_establishment = models.SmallIntegerField()
    pre_primary = models.CharField(max_length=10)
    building_status = models.CharField(max_length=60)
    boundary_wall = models.CharField(max_length=60)
    no_of_boys_toilets = models.SmallIntegerField()
    no_of_girls_toilets = models.SmallIntegerField()
    no_of_cwsn_toilets = models.SmallIntegerField()

    # need to remove these two fields since all values are yes
    drinking_water_availability = models.BooleanField(default=True) # yes no
    hand_wash_facility = models.BooleanField(default=True) #yes

    functional_generator = models.SmallIntegerField()
    library = models.BooleanField(default=True)
    reading_corner = models.BooleanField(default=True)
    book_bank = models.BooleanField(default=True)
    functional_laptop = models.SmallIntegerField()
    functional_desktop = models.SmallIntegerField()
    functional_tablet = models.SmallIntegerField()
    functional_scanner = models.SmallIntegerField()
    functional_printer = models.SmallIntegerField()
    functional_led = models.SmallIntegerField()
    functional_digiboard = models.SmallIntegerField()
    internet = models.BooleanField(default=True)
    dth = models.BooleanField(default=True)
    functional_web_cam = models.SmallIntegerField()
    class_rooms = models.SmallIntegerField()
    other_rooms = models.SmallIntegerField()
    enrolment_of_the_students = models.CharField(max_length=60)
    total_teachers = models.SmallIntegerField()

    def get_absolute_url(self):
        
        url = reverse('schools:school_view', kwargs={'code' : self.udise_code})
        return f"{url}{slugify(self.school_name)[:60]}"




class KeralaSchool(models.Model):
    
    name = models.CharField(max_length=200)
    code = models.IntegerField(unique=True)
    district = models.CharField(max_length=30)
    edu_district = models.CharField(max_length=30)
    sub_district = models.CharField(max_length=30)
    url_id = models.IntegerField(blank =True, null = True)
    # created_on = models.DateTimeField(auto_now_add = True)

    # # new fields on 11/oct/2021
    # updated_at = models.DateTimeField(blank=True, null=True)
    hs_phone = models.CharField(max_length=30, blank=True)
    hse_phone = models.CharField(max_length=30, blank=True)
    hs_email = models.CharField(max_length=200, blank=True)
    hse_email = models.CharField(max_length=200, blank=True)
    headmaster_name = models.CharField(max_length=200, blank=True)
    
    # use data scraped from https://schoolwiki.in/index.php?title=20001
    lat = models.CharField(max_length=30, blank=True)
    lon = models.CharField(max_length=30, blank=True)
    # use data scraped from https://sametham.kite.kerala.gov.in/20001
    location = models.CharField(max_length=200, blank=True)
    
    img_src = models.TextField(blank=True)
    mal_address = models.TextField(blank=True)
    website = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
    def get_location(self):
        """Get latitude and longitude from url"""
        startswith = 'http://maps.google.com/maps?q='
        if self.location.startswith(startswith):
            # http://maps.google.com/maps?q=10.795691,76.070796000000001
            return self.location.replace(startswith,'').split(',')
    
    def get_absolute_url(self):

        url = reverse('schools:school_view_kerala', kwargs={'code' : self.code})
        return f"{url}{slugify(self.name)[:60]}"

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (0, 'others'), #admin, superadmin etc, so ./manage.py createsuperuser will return default
      (1, 'student'),
      (2, 'teacher'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=0)
    # school = models.ForeignKey(School,on_delete=models.CASCADE, related_name='users',null=True,blank=True)
    mobile = models.PositiveBigIntegerField(null=True)
    
    @property
    def is_student(self):
        "Is the user a student?"
        return self.user_type == 1

    @property
    def is_teacher(self):
        "Is the user a teacher?"
        return self.user_type == 2   


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                from_user=self.user,
                to_user=feed.user,
                feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                from_user=self.user, 
                to_user=feed.user, 
                feed=feed).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                        from_user=self.user,
                        to_user=feed.user,
                        feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                from_user=self.user,
                to_user=User(id=user),
                feed=feed).save()

    