
from django.test import TestCase, Client
from django.urls import reverse

class BachelorsPortalTest(TestCase):
    fixtures = ["sample.json"]
    def setUp(self):
        self.client = Client()

    
    def test_colleges(self):
        jk_link = reverse('bachelorsportal:home')
        response = self.client.get(jk_link)
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'Colleges in Europe')
    
    def test_college_view(self):
        jk_link = reverse('bachelorsportal:college_view', kwargs={'code':'237799'})
        response = self.client.get(jk_link)
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'LLB (Hons) Law with Psychology')
        self.assertContains(response, 'University of Essex Online')

        self.assertContains(response, '4856')
        self.assertContains(response, '48')
        self.assertContains(response, 'The LLB (Hons) Law with Psychology programme from')
    


        