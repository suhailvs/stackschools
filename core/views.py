from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views import View
from django.db.models import Q

class UserList(ListView):
    # model = get_user_model()
    paginate_by = 36
    template_name = 'core/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q','')
        User = get_user_model()

        queryset = User.objects.order_by('first_name')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)|Q(last_name__icontains=query)|
                Q(username__icontains=query)|Q(email__icontains=query)
            )
        return queryset

    


class UserDetail(View):
    """Show Details of a Student"""
    def get(self, request, **kwargs):
        user = get_user_model().objects.get(id = kwargs['user'])
        return render(request,'core/user_detail.html', {'user_data': user})
