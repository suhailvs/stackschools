from django.shortcuts import render
from .models import PostalCode, Edit
from .country_codes import COUNTRY_CODES

from bachelorsportal.views import incr_counter
from django.views.generic.edit import CreateView
from django import forms

class PostalCodeCreateForm(forms.ModelForm):
    COLOR_CHOICES = [(key, value) for key, value in COUNTRY_CODES.items()]
                     


    country = forms.CharField(
        widget=forms.Select(choices=COLOR_CHOICES, attrs={"class": "form-select"})
    )
    class Meta:
        model = PostalCode
        fields = ['country','postal_code','place','admin_name1','admin_name2','admin_name3'] #'__all__'
    


class PostalCodeCreateView(CreateView):
    model = PostalCode
    form_class = PostalCodeCreateForm
    def form_valid(self, form):
        response = super().form_valid(form)
        Edit.objects.create(postal_code=self.object.postal_code)
        return response
    



def postalcode_view(request, code):
    incr_counter('postalcodes')
    data = PostalCode.objects.filter(postal_code=code)
    return render(request, "postalcodes/postalcode.html", {"data":data})

def home(request):
    return render(request,'postalcodes/home.html')