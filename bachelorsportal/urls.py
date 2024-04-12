from django.urls import include, path, re_path
from . import views

app_name = 'bachelorsportal'
urlpatterns = [
    re_path(r'^(?P<code>\d{6})/',views.college_view, name='college_view'),
    path('', views.home, name="home"),
]