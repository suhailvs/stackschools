
def a():
    from schools.models import KeralaSchool, School
    from django.db.models import Count
    district = 'palakkad'
    sub_districts_and_count = School.objects.filter(
        state__iexact='kerala',
        district__iexact=district,
    ).values('block').distinct().annotate(count=Count('district'))
    print(KeralaSchool.objects.filter(district__iexact=district).values_list('sub_district').distinct())
    for block_obj in sub_districts_and_count:
        block=block_obj['block']
        udise=School.objects.filter(state__iexact='kerala',district__iexact=district,block=block)
        kerala=KeralaSchool.objects.filter(district__iexact=district,sub_district__iexact=block)
        # print([s.school_name for s in udise])
        # print([s.name for s in kerala])
        
        print(udise.count(),kerala.count(), block)
    


def b():
    from django.contrib.gis.geos import Point
    from schools.models import KeralaSchool
    step = 1000
    total = KeralaSchool.objects.count()
    for i in range(0,total,step):
        print('going to update range:',i,i+step)
        objs =[obj for obj in KeralaSchool.objects.order_by('id')[i:i+step]]
        for obj in objs:
            if obj.lon:
                obj.GEOMETRY=Point(float(obj.lon), float(obj.lat))
            if obj.location:
                loc = obj.get_location()
                obj.GEOMETRY2 = Point(float(loc[1]), float(loc[0]))
        print(KeralaSchool.objects.bulk_update(objs, ["GEOMETRY","GEOMETRY2"]))
