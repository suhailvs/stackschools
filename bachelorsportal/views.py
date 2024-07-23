from django.shortcuts import render
from .models import BPCollege
from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from schools.models import GeneralSettings
def incr_counter(key):
    obj,created = GeneralSettings.objects.get_or_create(key=key)
    if created:
        obj.value = 1
    else:
        try:
            obj.value=int(obj.value)+1
        except:
            obj.value=1
    obj.save()

def home(request):
    return render(request, "bachelorsportal/home.html")

def college_view(request, code):   
    # college = df.loc[df["id"] == int(code)]["card"]
    incr_counter('college')
    data = BPCollege.objects.get(code=code)
    return render(request, "bachelorsportal/college.html", {"data":data})

class BPAjaxDatatableView(AjaxDatatableView):
    model = BPCollege
    title = 'Colleges in Europe'
    initial_order = [["title", "asc"], ]

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'title', 'visible': True, },
        {'name': 'university', 'visible': True, },
        {'name': 'city', 'visible': True, },
        {'name': 'country', 'visible': True, },
        {'name': 'view', 'title': '', 'searchable': False, 'orderable': False, },
        
    ]

    def customize_row(self, row, obj):
        # https://github.com/morlandi/django-ajax-datatable#id42
        row['view'] = f"<a class='btn btn-warning btn-sm' href='{obj.get_absolute_url()}'>View</a>"