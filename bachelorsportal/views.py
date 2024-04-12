from django.shortcuts import render
from django.http import HttpResponse
from .models import BPCollege

def home(request):
    return HttpResponse('home')


def college_view(request, code):   
    # college = df.loc[df["id"] == int(code)]["card"]
    data = BPCollege.objects.get(code=code)
    return render(request, "bachelorsportal/college.html", {"data":data})
