import yfinance as yf
from yfinance import Ticker

#SET UP TRACKER HERE:


def fiveback(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='5d', interval='1d')
    #print(data)
    close = data['Close'].iloc[0]
    #print(close)
    return close

def nownow(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.fast_info.last_price
    #print(data)
    return data

def color(symbol):
    if nownow(symbol) > fiveback(symbol):
        return "green"
    else:
        return "red"

def combine(name, symbol):
    print(name,": ")
    print(fiveback(symbol))
    print(nownow(symbol))
    print()
    print(color(symbol))
    print()
    print()

### CALLS
#symbols -- Telsa = TSLA, S&P 500 = ^GSPC, USD to EURO  is EUR=X
#
combine("Tesla", 'TSLA')
combine("S&P 500",'^GSPC')
combine("USD to EUR",'EUR=X')

