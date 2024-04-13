"""
Usage: 

    ./manage.py shell
    >>> from bachelorsportal import t
    >>> t.load_datas('engineering_&_technology_not_formatted_2100.json')
"""

from .models import BPCollege

class FormatJson:
    """
    input -> {
        "id": int,
        "enhanced":true,
        "card": {
            "class":str,
            "func":{...}
        }
    }
    output ->  {
        'id': int,
        'title':str,
        'summary':str,
        'fee':[
            {
                'amount':int
                'currency':str
                'unit':str
            }
        ]
    }

    Usage:
        >>> f = FormatJson(item)
        >>> f.format()
    """

    def __init__(self, data) -> None:
        self.data = data
        self.func = data["func"]

    def getfees(self):
        """
        Input -> None
        Output -> [
            {
                "target": item["func"]["getTarget"],
                "amount": item["func"]["getAmount"],
                "currency": item["func"]["getCurrency"],
                "unit": item["func"]["getUnit"]
            }
        ]
        """
        data = []
        fees = self.func["getTuitionFees"] or []
        for item in fees:
            data.append(
                {
                    "target": item["func"]["getTarget"],
                    "amount": item["func"]["getAmount"],
                    "currency": item["func"]["getCurrency"],
                    "unit": item["func"]["getUnit"],
                }
            )
        return data

    def getdur(self):
        dur = self.func["getDuration"]
        if not dur: return {'period':'', 'amount':None}
        func = dur["func"]
        return {
            "period": func["getPeriod"],
            "amount": func["getAmount"],
        }

    def getuniversity(self):
        func = self.func["getUniversityLink"]["func"]
        return func['getDescription']
    
    def getloc(self):
        func = self.func["getLocation"]["func"]
        city = func['getCity']['func']['getDescription']
        country = func['getCountry']['func']['getDescription']
        return {
            "city": city,
            "country": country,
        }
    def format(self):
        logo = self.func["getLogo"]["func"]["getSource"] if self.func["getLogo"] else ''
        return {
            # "id": self.data["id"],
            "title": self.func["getTitle"],
            "degree": self.func["getDegree"],
            "summary": self.func["getSummary"],
            "fee": self.getfees(),
            "duration": self.getdur(),
            "university": self.func["getUniversityLink"]["func"]["getDescription"],
            "logo": logo,
            "location": self.getloc(),
            'fullonline': self.func["isFullyOnline"] if "isFullyOnline" in self.func else None,
            'online': self.func["isOnline"] if "isOnline" in self.func else None,
            'oncampus': self.func["isOnCampus"] if "isOnCampus" in self.func else None,
            # 'isBlended': self.func["isBlended"],
            'fulltime': self.func["isFullTime"] if "isFullTime" in self.func else None,
            'parttime': self.func["isPartTime"] if "isPartTime" in self.func else None,
            "ielts": self.func["getEnglishRequirements"]['func']['getIELTS'] if "getEnglishRequirements" in self.func else None,
            "toefl": self.func["getEnglishRequirements"]['func']['getTOEFLInternet'] if "getEnglishRequirements" in self.func else None,            
        }
def load_datas(fname):
    import pandas as pd
    # fname = "bachelorsportal/uk_not_formatted_8000.json"
    df = pd.read_json(fname)
    for index, c in df.iterrows():
        data = dict(c)
        print(index,data["id"],'\n','='*10)
        colleage_formatter = FormatJson(data["card"])
        d = colleage_formatter.format()
        fee_int=None
        fee_int_currency=''
        fee_nat=None
        fee_nat_currency=''
        for fee in d['fee']:
            if fee['target']=='international':
                fee_int = fee['amount']
                fee_int_currency = fee['currency']
            elif fee['target']=='national':
                fee_nat = fee['amount']
                fee_nat_currency = fee['currency']
        if BPCollege.objects.filter(code=data['id']).exists():
            print("item exists")
        else:
            BPCollege.objects.create(
                code = data["id"],
                title = d['title'],
                degree = d['degree'],
                summary = d['summary'],
                duration = d['duration']['amount'],
                university = d['university'],
                university_logo = d['logo'],
                city = d['location']['city'],
                country = d['location']['country'],
                fullonline = d['fullonline'],
                online = d['online'],
                oncampus = d['oncampus'],
                fulltime = d['fulltime'],
                parttime = d['parttime'],
                ielts = d['ielts'],
                toefl = d['toefl'],
                fee_int=fee_int,
                fee_int_currency=fee_int_currency,
                fee_nat=fee_nat,
                fee_nat_currency=fee_nat_currency,
            )
