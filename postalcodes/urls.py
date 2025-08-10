from django.urls import path, re_path, include
from . import views

app_name = 'postalcodes'
urlpatterns = [
    path('',views.home),
    path("add/", views.PostalCodeCreateView.as_view(), name="postalcode_add"), 
    path('<code>/',views.postalcode_view, name='postalcode_view'),  
]

