"""
USAGE:

- cloned git repo git@github.com:sta-k/sta-k.github.io.git/

- set MY_PATH to the repo url

    $ ./manage.py shell
    >>> from sitegenerator import c
    >>> c.save()
"""

from schools.models import School, KeralaSchool

from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.text import slugify
import os
import shutil

MY_PATH= '/home/suhail/Desktop/sta-k.github.io/' # url of git repo git@github.com:sta-k/sta-k.github.io.git/
FOLDER = 'schools/'

class StaticGenerator:
    def create_file(self, fname, html):
        fp = open(f'{MY_PATH}{fname}', 'w')
        fp.write(html)


    def save_homepage(self):
        # os.makedirs(MY_PATH)
        context = {}
        context['total_schools']=School.objects.count()
        context['states']=School.objects.values('state').distinct().annotate(count=Count('state'))
        rendered = render_to_string('home.html',context)
        self.create_file('index.html', rendered)
        self.save_districts(context['states'])

    def save_districts(self, states):
        os.makedirs(f'{MY_PATH}{FOLDER}')
        for state_schools in states:
            state = slugify(state_schools['state'])
            schools = School.objects.filter(state__icontains=state.split('-')[0])
            districts_and_count = schools.values('state','district').distinct().annotate(count=Count('district'))
            rendered = render_to_string('schools/districts.html',{
                'districts':districts_and_count, 
                'state': state,
                'total_schools':schools.count()
            })
            os.makedirs(f'{MY_PATH}{FOLDER}{state}')
            print(state)
            self.create_file(f'{FOLDER}{state}/index.html', rendered)
            self.save_sub_districts(state,districts_and_count)
            break

    def save_sub_districts(self,state, districts):
        # path('<slug:state>/<district>/',school_views.sub_districts, name='sub_districts'),
        # sub_districts with school count
        for district in districts:
            district = district['district']
            sub_districts_and_count = School.objects.filter(
                state__icontains=state.split('-')[0],
                district=district
            ).values('block').distinct().annotate(count=Count('district')) # ., sub_district__iexact = sub_district)
            rendered = render_to_string('schools/sub_districts.html',{'district':district,'state':state,
                'sub_districts':sub_districts_and_count})
            os.makedirs(f'{MY_PATH}{FOLDER}{state}/{district}')
            self.create_file(f'{FOLDER}{state}/{district}/index.html', rendered)
            self.save_schools(state,district,sub_districts_and_count)

    def save_schools(self,state,district,sub_districts):

        for sub_district in sub_districts:
            sub_district = sub_district['block']
            school_list = School.objects.filter(
                state__icontains=state.split('-')[0],
                district=district,
                block = sub_district
            ).order_by('school_name')

            rendered = render_to_string('schools/schools.html',{'schools':school_list, 'district':district,'state':state,
            'sub_district':sub_district})
            os.makedirs(f'{MY_PATH}{FOLDER}{state}/{district}/{sub_district}')
            # print(sub_district)
            self.create_file(f'{FOLDER}{state}/{district}/{sub_district}/index.html', rendered)
            self.save_schools_data(school_list)
            
    def save_schools_data(self, schools):
        for school in schools:
            context = {'school':school}
            context['class_students']=[int(s) for s in context['school'].enrolment_of_the_students.split(',')]
            context['total_students']=sum(context['class_students'])
            rendered = render_to_string('schools/school_udise.html',context)
            os.makedirs(f'{MY_PATH}{FOLDER}{school.udise_code}')
            
            name_slug = slugify(school.school_name[:60])
            self.create_file(f'{FOLDER}{school.udise_code}/index.html', f'<meta http-equiv="refresh" content="0; url=./{name_slug}/" />')
            os.makedirs(f'{MY_PATH}{FOLDER}{school.udise_code}/{name_slug}')
            self.create_file(f'{FOLDER}{school.udise_code}/{name_slug}/index.html', rendered)

    def save_kerala_schools_data(self):
        for school in KeralaSchool.objects.all():
            rendered = render_to_string('schools/school.html',{'school':school})
            os.makedirs(f'{MY_PATH}{FOLDER}{school.code}')
            self.create_file(f'{FOLDER}{school.code}/index.html', rendered)
            name_slug = slugify(school.name[:60])
            # self.create_file(f'{FOLDER}{school.code}/{name_slug}', rendered)
            os.makedirs(f'{MY_PATH}{FOLDER}{school.code}/{name_slug}')
            self.create_file(f'{FOLDER}{school.code}/{name_slug}/index.html', rendered)
            break

    def save(self):
        try:
            shutil.rmtree(f'{MY_PATH}{FOLDER}')
        except:
            print('folder not found')
        self.save_homepage()
        self.save_kerala_schools_data()
c=StaticGenerator()


