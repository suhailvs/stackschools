"""
Installation: 
    pip -v install gevent
    pip install locust
Usage:
    $ locust -f locustfile.py
    visit http://localhost:8089/
"""

from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    
    @task
    def classroom(self):
        self.client.get("schools/kerala/ALAPPUZHA/")
