from django.urls import include, path
from django.views.generic import TemplateView

from core.views import UserList, UserDetail
app_name='core'

urlpatterns = [
	path('', UserList.as_view(), name='users'),
	path('<int:user>/', UserDetail.as_view(), name='user_detail'),
]

