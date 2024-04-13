import requests
import json

from .utils import SUBJECTS

class ScrapIt:
    """
    usage:
        >>> from bachelorsportal.scrap import ScrapIt
        >>> s = ScrapIt(q = 'computer_science_&_it', size=100, start=0)
        >>> s.scrap() # will generate json file
    """

    def __init__(self, q,url="https://search.prtl.co/2023-02-23/", size=20, start=0) -> None:
        """
        api url and params which get from
        https://www.bachelorsportal.com/search/bachelor/united-kingdom
        avilable countries can get from https://www.bachelorsportal.com/countries/
        """

        self.url = url
        self.q = q  # query param. eg: en-2249|ci-30|lv-bachelor|tc-EUR|uc-108
        self.size = size  # items per page
        self.start = start  # pagination start

    def get_json_data(self):
        start = self.start
        json_data = []
        while True:
            try:
                new_data = self.make_request(start)
                if new_data:
                    json_data += new_data
                else:
                    return json_data
                print("items:", len(json_data), "size:", self.size, "start:", start)
                start = start + self.size  
            except Exception as e:
                print(e)
                return json_data

    def make_request(self, start):
        payload = {"q": f"en-912|{SUBJECTS[self.q]}|lv-bachelor|tc-EUR|uc-108", "size": self.size, "start": start}
        r = requests.get(self.url, params=payload)
        
        return r.json()

    def save_json_data(self, json_data, json_type="not_formatted"):
        """save json to file"""
        filename = f"{self.q}_{json_type}_{len(json_data)}"
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def scrap(self):
        json_data = self.get_json_data()
        self.save_json_data(json_data)