from django.urls import path, include
from rest_framework import routers
from .views import MarkersMapView, MarkerViewSet

app_name = "myapp"

router = routers.DefaultRouter()
router.register(r"markers", MarkerViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", MarkersMapView.as_view()),
]
