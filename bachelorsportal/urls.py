from django.urls import include, path, re_path
from . import views

app_name = 'bachelorsportal'
urlpatterns = [
    path('', views.home, name="home"),
    re_path(r'^(?P<code>\d{4,6})/',views.college_view, name='college_view'),    
    path('ajax_datatable/', views.BPAjaxDatatableView.as_view(), name="ajax_datatable"),
]

