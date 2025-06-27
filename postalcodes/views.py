from django.shortcuts import render
from .models import PostalCode

def postalcode_view(request, code):   
    data = PostalCode.objects.filter(postal_code=code)
    return render(request, "postalcodes/postalcode.html", {"data":data})

def home(request):
    return render(request,'postalcodes/home.html')