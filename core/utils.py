import requests
import os
import decimal
from bs4 import BeautifulSoup
import chardet
import lxml

def lookup1(symbol):
    # check if symbol contains a non alphabet character
    if not symbol.isalpha():
        return "INVALID SYMBOL"

    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=QRM8PZIX9EXKT0SI' % symbol
    r = requests.get(url)

    quote = r.json()

    if r.status_code != 200:
        return "API LIMIT"
    elif quote == {}:
        return "INVALID SYMBOL"
    elif quote["Global Quote"] == {}:
        return "INVALID SYMBOL"
    
    price = quote["Global Quote"]["05. price"]
    price = price[:-2]
    return decimal.Decimal(price)

# web scraping NOT USED
def lookup(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = "https://uk.finance.yahoo.com/quote/%s" % symbol

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    try:
            price = soup.find('fin-streamer', {'class': "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text

    except:
        return "INVALID SYMBOL"

    return decimal.Decimal(price)

