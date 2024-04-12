from django.shortcuts import render
from .models import BPCollege

def home(request):
    return render(request, "bachelorsportal/home.html")


def college_view(request, code):   
    # college = df.loc[df["id"] == int(code)]["card"]
    data = BPCollege.objects.get(code=code)
    return render(request, "bachelorsportal/college.html", {"data":data})
