import requests
import os
import decimal

def lookup(symbol):


    import requests

    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=QRM8PZIX9EXKT0SI' % symbol
    r = requests.get(url)
    data = r.json()

    quote = r.json()

    try:
        print(r.status_code)
        print(quote)
        print(quote["Global Quote"]["05. price"])
    except:
        print("API call failed.")

    if r.status_code != 200:
        return "API LIMIT"
    elif quote["Global Quote"] == {}:
        return "INVALID SYMBOL"
    
    price = quote["Global Quote"]["05. price"]
    price = price[:-2]
    return decimal.Decimal(price)
