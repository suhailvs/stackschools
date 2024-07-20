
from django.urls import include, path

from feeds import views
app_name='feeds'

urlpatterns = [
    path('', views.feeds, name='feeds'),
    path('post/', views.post, name='post'),
    path('like/', views.like, name='like'),
    path('comment/', views.comment, name='comment'),
    path('load/', views.load, name='load'),
    path('check/', views.check, name='check'),
    path('load_new/', views.load_new, name='load_new'),
    path('update/', views.update, name='update'),
    path('track_comments/', views.track_comments, name='track_comments'),
    path('remove/', views.remove, name='remove_feed'),
    path('<int:pk>/', views.feed, name='feed'),
]