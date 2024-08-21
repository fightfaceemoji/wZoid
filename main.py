import yfinance as yf
from yfinance import Ticker
import time
from threading import Timer
import tkinter as tk

# Store prices for different symbols
tracked_data = {
    'TSLA': {'name': 'Tesla', 'price': 221.1},
    '^GSPC': {'name': 'S&P 500', 'price': 5597.12},
    'EUR=X': {'name': 'USD to EUR', 'price': 0.8988},
    'BRK-B': { 'name':'Berkshire B', 'price': 448.00},
    'AAPL':{'name':'Apple','price':226.51}
}

##variables
on = True
user_input = 'q'

## this finds the close from five days ago
def fiveback(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='5d', interval='1d')
    #print(data)
    close = data['Close'].iloc[0]
    #print(close)
    return close

## the most recent price pulled
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

## this function just combines the functions for the prints, its mostly for checking run
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
            #combine(symbol, tracked_data[symbol]['name'])
            tracked_data[symbol]['color'] = color(symbol)
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
            break
        else:
            print("Refreshing...")

def fresh_gui():
    refresh()
    for i, symbol in enumerate(tracked_data.keys()):
        set_price(symbol,price_entries[i].get())
        refresh()
        data = tracked_data[symbol]
        name_label = name_labels[i]
        symbol_label = symbol_labels[i]
        color_box = color_boxes[i]
        name_label.config(text=data['name'])
        symbol_label.config(text=symbol)
        color_box.config(bg=data['color'])


def stop_program():
    global on
    on = False
    root.destroy()

def set_price(symbol, new_price):
    try:
        new_price = float(new_price)
        if symbol in tracked_data:
            tracked_data[symbol]['price'] = new_price
            print(f"Success: Updated {tracked_data[symbol]['name']} to {new_price}")
        else:
            print(f"Error: Symbol {symbol} not found!")
    except ValueError:
        print("Error: Please enter a valid number for the price.")

# Create the main window
root = tk.Tk()
root.title("Stock Tracker")

# Create and place widgets
name_labels = []
symbol_labels = []
color_boxes = []
price_entries = []

for i, symbol in enumerate(tracked_data.keys()):
    tk.Label(root, text=tracked_data[symbol]['name']).grid(row=i, column=0)
    tk.Label(root, text=symbol).grid(row=i, column=1)
    color_box = tk.Label(root, width=10, height=2, relief="solid")
    color_box.grid(row=i, column=2)

    # Create an Entry widget and store it in the list
    price_entry = tk.Entry(root)
    price_entry.grid(row=i, column=3)
    price_entries.append(price_entry)

    name_labels.append(tk.Label(root))
    symbol_labels.append(tk.Label(root))
    color_boxes.append(color_box)

# Add a button to exit the program
exit_button = tk.Button(root, text="Exit", command=stop_program)
exit_button.grid(row=len(tracked_data), column = 1)
refresh_button = tk.Button(root, text="Refresh", command=lambda: fresh_gui())
refresh_button.grid(row=len(tracked_data), column=3)

##go, be free
fresh_gui()
root.mainloop()
