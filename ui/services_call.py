import requests
import json

with open('./config.json') as f:
    config = json.load(f)

class Simcel:
    host = config['cel_api']
    
    @staticmethod
    def pie_chart_1(attr):
        """
        return data for Outlet pie charts
        """
        url = f"{Simcel.host}/pie"

        payload = json.dumps({
            "data": attr
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)
        if dta['status']==200:
            jdata = json.loads(dta['data'])
            # df = pd.DataFrame(jdata)
            return jdata
        else:
            return None

    @staticmethod
    def pie_chart_2(attr):
        """
        return data for Outlet pie charts
        """
        url = f"{Simcel.host}/pie2"

        payload = json.dumps({
            "data": attr
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)
        if dta['status']==200:
            jdata = json.loads(dta['data'])
            # df = pd.DataFrame(jdata)
            return jdata
        else:
            return None

    @staticmethod
    def outlet_sales():
        """
        return data for Outlet pie charts
        """
        url = f"{Simcel.host}/outlet_sales"

        payload = {}
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)
        if dta['status']==200:
            return json.loads(dta['data'])
        else:
            return None
    
    @staticmethod
    def simcel_data():
        """
        return cleaned simcel data
        """
        url = f"{Simcel.host}/simcel"

        payload={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)
        if dta['status']==200:
            return json.loads(dta['data'])
        else:
            return None

    @staticmethod
    def items_data():
        """
        return items information
        """
        url = f"{Simcel.host}/items"

        payload={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)
        if dta['status']==200:
            return json.loads(dta['data'])
        else:
            return None
    
    @staticmethod
    def outlets_data():
        """
        return outlets information
        """
        url = f"{Simcel.host}/outlets"

        payload={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)
        if dta['status']==200:
            return json.loads(dta['data'])
        else:
            return None
        

class Yfin:
    host = config['yfin_api']

    @staticmethod
    def fetch(code, period):
        """
        return outlets information
        """
        url = f"{Yfin.host}/data"

        payload = json.dumps({
            "code": code,
            "period": period
        })
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)

        if dta['status']==200:
            return json.loads(dta['data'])
        else:
            return None

    @staticmethod
    def get_company_info(code):
        """
        return outlets information
        """
        url = f"{Yfin.host}/company"

        payload = json.dumps({
            "code": code,
            "period": ""
        })
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        
        dta = json.loads(response.text)

        if dta['status']==200:
            dta = json.loads(dta['data'])
            return dta
        else:
            return None
