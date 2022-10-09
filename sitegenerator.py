from schools.models import School, KeralaSchool

from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.text import slugify

def save_homepage():
    context = {}
    context['total_schools']=School.objects.count()
    context['states']=School.objects.values('state').distinct().annotate(count=Count('state'))
    rendered = render_to_string('home.html',context)
    fp = open('index.html', 'w')
    fp.write(rendered)

def save_districts():
    # districts with school count
    states = School.objects.values('state').distinct().annotate(count=Count('state'))
    for state_schools in states:
        state = slugify(state_schools['state'])
        schools = School.objects.filter(state__icontains=state.split('-')[0])
        districts_and_count = schools.values('state','district').distinct().annotate(count=Count('district'))
        rendered = render_to_string('schools/districts.html',{
            'districts':districts_and_count, 
            'state': state,
            'total_schools':schools.count()
        })
        print(state)
        fp = open(f'{state}.html', 'w')
        fp.write(rendered)

"""
def save_sub_districts(request,state,district):
    # sub_districts with school count
    sub_districts_and_count = School.objects.filter(
        state__icontains=state.split('-')[0],
        district=district
    ).values('block').distinct().annotate(count=Count('district')) # ., sub_district__iexact = sub_district)
    return render(request,'schools/sub_districts.html',{'district':district,'state':state,
        'sub_districts':sub_districts_and_count})

def save_schools(request,state,district,sub_district):
    school_list = School.objects.filter(
        state__icontains=state.split('-')[0],
        district=district,
        block = sub_district
    ).order_by('school_name')

    # filtered by name
    name = request.GET.get('name','')
    if name: 
        school_list = school_list.filter(school_name__icontains = name)
    
    return render(request,'schools/schools.html',{'schools':school_list, 'district':district,'state':state,
        'sub_district':sub_district})

def save_school_view(request,code):
    udise=code
    # udise school
    context = {'school':School.objects.get(udise_code=udise)}
    context['class_students']=[int(s) for s in context['school'].enrolment_of_the_students.split(',')]
    context['total_students']=sum(context['class_students'])
    
    return render(request,'schools/school_udise.html',context)


def save_school_view_kerala(request,code):
    # kerala school
    return render(request,'schools/school.html',{'school':KeralaSchool.objects.get(code = code)})
"""