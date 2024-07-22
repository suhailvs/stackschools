def a():
    from schools.models import KeralaSchool
    print(KeralaSchool.objects.filter(location='').count())
    print(KeralaSchool.objects.filter(location='',lon='').count())
def b():
    from django.contrib.gis.geos import Point
    from schools.models import KeralaSchool
    notfound=0
    
    objs =[obj for obj in KeralaSchool.objects.order_by('id')]
    
    for obj in objs:
        obj.GEOMETRY=None
        if obj.location:
            loc = obj.get_location()
            obj.GEOMETRY = Point(float(loc[1]), float(loc[0]))
        else:
            notfound+=1
        # elif obj.lon:
        #     obj.GEOMETRY=Point(float(obj.lon), float(obj.lat))
    print(KeralaSchool.objects.bulk_update(objs, ["GEOMETRY"]))
    print(notfound)


def load():
    import csv
    from schools.models import KeralaSchool
    with open('kerala.csv') as csvfile:
        reader = csv.reader(csvfile,)
        for row in reader:
            code = row[2]
            if code:
                s=KeralaSchool.objects.get(code = code)
                s.udise_code=row[3]
                s.save()
                print(row)
