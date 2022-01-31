
from django.template.defaultfilters import register
from schools.models import GeneralSettings

@register.simple_tag
def google_analytics_status():
    ga = GeneralSettings.objects.filter(key='google_analytics_status').first()
    if ga and ga.value=='true':
        return True
    return False