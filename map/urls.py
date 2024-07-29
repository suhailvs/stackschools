from django.urls import path, include
from rest_framework import routers
from .views import home, MarkerViewSet

app_name = "map"

router = routers.DefaultRouter()
router.register(r"markers", MarkerViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", home, name='home'),
]
