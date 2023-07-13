import requests
import os
import decimal
from bs4 import BeautifulSoup
import chardet
import lxml

def lookup(symbol):


    import requests

    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=QRM8PZIX9EXKT0SI' % symbol
    r = requests.get(url)
    data = r.json()

    quote = r.json()

    print(quote)

    if r.status_code != 200:
        return "API LIMIT"
    elif quote == {}:
        return "INVALID SYMBOL"
    elif quote["Global Quote"] == {}:
        return "INVALID SYMBOL"
    
    price = quote["Global Quote"]["05. price"]
    price = price[:-2]
    return decimal.Decimal(price)

def lookup1(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = "https://uk.finance.yahoo.com/quote/%s" % symbol

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    price = soup.find('fin-streamer', {'class': "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text

    return decimal.Decimal(price)
