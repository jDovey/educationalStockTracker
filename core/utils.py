import requests
import os

def lookup(symbol):


    import requests

    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function":"GLOBAL_QUOTE","symbol":symbol,"datatype":"json"}

    headers = {
        "X-RapidAPI-Key": os.environ.get('API_KEY'),
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    quote = response.json()

    try:
        print(quote["Global Quote"]["05. price"])
    except:
        print("API call failed.")
