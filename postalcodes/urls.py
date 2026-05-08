from django.urls import path
from . import views

app_name = 'postalcodes'
urlpatterns = [
    path('',views.home),
    path('<code>/',views.postalcode_view, name='postalcode_view'),  
]

