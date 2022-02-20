from django.urls import include, path, re_path
from . import views as school_views
from django.views.generic import TemplateView

app_name = 'schools'
urlpatterns = [
	# if blank show districts(Thissur, palakkad...)
	# path('', school_views.states, name='states'),	
	# if digit, view school information
	re_path(r'^(?P<code>\d{5})/',school_views.school_view_kerala, name='school_view_kerala'),

	re_path(r'^(?P<code>\d{4}\w{7})/',school_views.school_view, name='school_view'),

	# if districts show districts(Thissur, palakkad...) of a state
	path('<slug:state>/', school_views.districts, name='districts'),

	# if character, show sub districts
	path('<slug:state>/<district>/',school_views.sub_districts, name='sub_districts'),
	path('<slug:state>/<district>/<sub_district>/',school_views.schools, name='schools'),
]