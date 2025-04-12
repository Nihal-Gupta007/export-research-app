# comtrade_api.py
import requests

def fetch_comtrade_data(params, api_key):
    base_url = "https://comtradeapi.un.org/public/v1/preview/C"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

