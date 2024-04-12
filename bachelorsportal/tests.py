
from django.test import TestCase, Client
from django.urls import reverse

class BachelorsPortalTest(TestCase):
    fixtures = ["sample.json"]
    def setUp(self):
        self.client = Client()

    # def test_site_root_url_works(self):
    #     response = self.client.get(reverse("bachelorsportal:home"))
    #     self.assertEqual(response.status_code, 200)
    
    def test_college_view(self):
        jk_link = reverse('bachelorsportal:college_view', kwargs={'code':'237799'})
        response = self.client.get(jk_link)
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'LLB (Hons) Law with Psychology')
        self.assertContains(response, 'University of Essex Online')

        self.assertContains(response, '4856')
        self.assertContains(response, '48')
        self.assertContains(response, 'The LLB (Hons) Law with Psychology programme from')

        