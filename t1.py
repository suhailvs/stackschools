
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
    

a()