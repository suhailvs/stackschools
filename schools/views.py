

from django.shortcuts import render, redirect
from django.db.models import Count, Q

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from bachelorsportal.views import incr_counter
from .models import School, KeralaSchool
# Create your views here.

class SignUpForm(UserCreationForm):
   class Meta:
      model = get_user_model()
      fields = ('username', 'password1', 'password2')

def home(request):
    context = {}
    # context['states'] = School.objects.values('state').distinct().annotate(count=Count('state'))
    if 'school_name' in request.GET:
        context['schools'] = School.objects.filter(
            Q(school_name__icontains = request.GET['school_name'])|
            Q(udise_code=request.GET['school_name']))[:100]
    else:
        context['total_schools']=School.objects.count()
        context['states']=School.objects.values('state').distinct().annotate(count=Count('state'))
    return render(request,'home.html',context) #{'states':states_and_count})

def states(request):
    context = {}
    context['states']=School.objects.values('state').distinct().annotate(count=Count('state'))
    context['total_schools']=School.objects.count()
    return render(request,'schools/states.html',context) #{'states':states_and_count})

def districts(request, state):
    # districts with school count
    schools = School.objects.filter(state__icontains=state.split('-')[0])
    districts_and_count = schools.values('state','district').distinct().annotate(count=Count('district'))
    return render(request,'schools/districts.html',{
        'districts':districts_and_count, 
        'state': state,
        'total_schools':schools.count()
    })

def sub_districts(request,state,district):
    # sub_districts with school count
    sub_districts_and_count = School.objects.filter(
        state__icontains=state.split('-')[0],
        district=district
    ).values('block').distinct().annotate(count=Count('district')) # ., sub_district__iexact = sub_district)
    return render(request,'schools/sub_districts.html',{'district':district,'state':state,
        'sub_districts':sub_districts_and_count})

def schools(request,state,district,sub_district):
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

def school_view(request,code):
    # udise school
    incr_counter('udise_school')    
    context = {'school':School.objects.get(udise_code=code)}
    context['class_students']=[int(s) for s in context['school'].enrolment_of_the_students.split(',')]
    context['total_students']=sum(context['class_students'])
    
    return render(request,'schools/school_udise.html',context)


def school_view_kerala(request,code):
    # kerala school
    incr_counter('kerala_school')
    return render(request,'schools/school_kerala.html',{'kschool':KeralaSchool.objects.get(code = code)})
