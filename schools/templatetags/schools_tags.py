
from django.template.defaultfilters import register
from schools.models import GeneralSettings
from postalcodes.country_codes import country_code_to_name
@register.simple_tag
def google_analytics_status():
    ga = GeneralSettings.objects.filter(key='google_analytics_status').first()
    if ga and ga.value=='true':
        return True
    return False


@register.filter(name="getcountryname")
def getcountryname(value):
    return country_code_to_name(value)