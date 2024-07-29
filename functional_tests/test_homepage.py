
import unittest, time
from selenium import webdriver
from selenium.webdriver.common.by import By


class HomePageTest(unittest.TestCase):  
    def setUp(self):  
        self.browser = webdriver.Firefox()  
        self.base_url = "https://stackschools.com/" # "http://localhost:8000/" #

    def tearDown(self):  
        self.browser.quit()

    def test_a_home_page(self):  
        # check out its homepage
        # naming a,b,c, in test function is because test is running in asc order
        self.browser.get(self.base_url)  

        self.assertIn("Stack Schools", self.browser.title)  
        states = ['Delhi','Haryana','Himachal Pradesh']
        states_ul = self.browser.find_element(By.TAG_NAME, "ul")  
        for state in states:
            self.assertIn(state, states_ul.text)
        time.sleep(5)
        
    def test_b_udise_school(self):
        self.browser.get(f'{self.base_url}schools/32060200110/')
        name_h2 = self.browser.find_element(By.TAG_NAME, "h2")  
        self.assertEqual('ASMMHSS ALATHUR', name_h2.text)
        time.sleep(5)
    
    def test_c_kerala_school(self):
        self.browser.get(f'{self.base_url}schools/21009/')
        name_h2 = self.browser.find_element(By.TAG_NAME, "h2")  
        self.assertEqual('A. S. M.M H. S.S Alathur', name_h2.text)
        time.sleep(5)

    def test_d_bp_college(self):
        self.browser.get(f'{self.base_url}bp/351803/')
        university_h3 = self.browser.find_element(By.TAG_NAME, "h3")  
        self.assertEqual('University of Limerick', university_h3.text)
        time.sleep(5)
        

if __name__ == "__main__":  
    unittest.main()  