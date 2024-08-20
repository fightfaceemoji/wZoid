import yfinance as yf
from yfinance import Ticker


#symbols -- Telsa = TSLA, S&P 500 = ^GSPC, USD to EURO  is EUR = X
def weekAgo(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='7d', interval='1d')
    print(data)


# create ticker for Tesla Stock
tTicker = yf.Ticker('TSLA')
# get data of the most recent date
tData = tTicker.history(period='7d', interval='1d')
#print data
print("TESLA")
print(tData)
# Extracting the closing price
tClose = tData['Close'].iloc[0]
print("TESLA Closing Price:", tClose)



spTicker = yf.Ticker('^GSPC')
spData = spTicker.history(period='1d')
print("S&P 500")
print(spData)
spClose = spData['Close'].iloc[0]
print("S&P 500 Closing Price:", spClose)


ueTicker = yf.Ticker('EUR=X')
ueData = ueTicker.history(period='1d')
print("USD to EUR")
print(ueData)
ueClose = ueData['Close'].iloc[0]
print("USD to EUR Closing Price:", ueClose)
