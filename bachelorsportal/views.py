from django.shortcuts import render
from .models import BPCollege
# Create your views here.
def college_view(request, code): 
    data = BPCollege.objects.get(code=code)
    return render(request, "bachelorsportal/college.html", {"data":data})