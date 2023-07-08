import requests
import os
import decimal

def lookup(symbol):


    import requests

    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function":"GLOBAL_QUOTE","symbol":symbol,"datatype":"json"}

    # DO NOT COMMIT API KEY
    
    headers = {
        "X-RapidAPI-Key": os.environ.get('API_KEY'),
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    quote = response.json()

    try:
        print(response.status_code)
        print(quote)
        print(quote["Global Quote"]["05. price"])
    except:
        print("API call failed.")

    if response.status_code != 200:
        return "API LIMIT"
    elif quote["Global Quote"] == {}:
        return "INVALID SYMBOL"
    
    price = quote["Global Quote"]["05. price"]
    price = price[:-2]
    return decimal.Decimal(price)
