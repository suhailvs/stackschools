
from django.test import TestCase, Client
import json
from django.urls import reverse
from django.template import Template, Context
from .models import School,KeralaSchool,User
class SchoolTest(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.client = Client()
    
    def test_site_root_url_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_search_page_content(self):
        # search page
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'Statewise Schools')
        self.assertNotContains(response, "Not on the page")
    

    # def test_search_result_content(self):
    #     # search result working
    #     response = self.client.get(reverse("q")+'?school_name=Hamidia+Public')
    #     self.assertContains(response, '<small>Hamidia Public School Rampore</small>') 
    
    def test_states_page(self):
        # page to list states is missing
        response = self.client.get(reverse('schools:states'))
        jk_link = reverse('schools:districts', kwargs={'state':'jammu-kashmir'})
        self.assertInHTML(f'<a href="{jk_link}">Jammu & Kashmir</a>', response.content.decode())

    def test_districts_page(self):
        # page to list districts in state
        response = self.client.get(reverse('schools:districts', kwargs={'state':'jammu-kashmir'}))

        baramula_link = reverse("schools:sub_districts", kwargs={'state':'jammu-kashmir',"district":"BARAMULA"})
        self.assertContains(response,baramula_link)
        self.assertInHTML(f'<a href="{baramula_link}">Baramula</a>', response.content.decode())
    
    def test_sub_districts_page(self):
        # page to list sub districts in districts
        response = self.client.get(reverse('schools:sub_districts', kwargs={'state':'jammu-kashmir',"district":"BARAMULA"}))
        dangerpora_link = reverse("schools:schools", kwargs={'state':'jammu-kashmir',"district":"BARAMULA","sub_district":"DANGERPORA"})
        self.assertInHTML(f'<a href="{dangerpora_link}">Dangerpora</a>', response.content.decode())


    def test_schools_in_subdistrict_page(self):
        # page to list schools in sub districts
        response = self.client.get(reverse("schools:schools", kwargs={'state':'jammu-kashmir',"district":"BARAMULA","sub_district":"DANGERPORA"}))

        hamidia_link = reverse('schools:school_view', kwargs={'code':'01020503406'})
        self.assertInHTML(f'''<a href="{hamidia_link}hamidia-public-school-rampore">
                <small>Hamidia Public School Rampore</small>
              </a>''', response.content.decode())
    
    def test_school_page(self):
        response = self.client.get(reverse('schools:school_view', kwargs={'code':'01020503406'}))
        self.assertContains(response, '<p class="lead">UDISE Code: <span class="badge bg-secondary">01020503406</span></p>')
    
    def test_keralaschool_page(self):
        response = self.client.get(reverse('schools:school_view_kerala', kwargs={'code':'21008'}))
        self.assertContains(response, '<li class="list-group-item list-group-item-dark">Head Master: <strong>GEETHA DEVI K B</strong></li>')