import yfinance as yf
from yfinance import Ticker
import time
from threading import Timer

# Store prices for different symbols
tracked_data = {
    'TSLA': {'name': 'Tesla', 'price': 750.0},
    '^GSPC': {'name': 'S&P 500', 'price': 4500.0},
    'EUR=X': {'name': 'USD to EUR', 'price': 0.85}
}

on = True
user_input = 'q'


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

#color code based on comparison
def color(symbol):
    if nownow(symbol) > tracked_data[symbol]['price']:
        return "green"
    else:
        return "red"

def combine(symbol, name):
    print(name,": ")
    print("five days ago close")
    print(fiveback(symbol))
    print("latest price")
    print(nownow(symbol))
    print()
    print(color(symbol))
    print()
    print()

def refresh():
    if on:
        for symbol in tracked_data.keys():
            combine(symbol, tracked_data[symbol]['name'])
        Timer(30, refresh).start()

def program():
    refresh()
    global user_input
    while user_input != 'x':
        user_input = input("Enter 'X' to exit at any time.").strip().lower()
        if user_input == 'x':
            print("Exiting now...")
            global on
            on = False
    print("Refreshing...")


##go, be free
program()
