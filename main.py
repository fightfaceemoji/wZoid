import yfinance as yf
from threading import Timer
import tkinter as tk
from datetime import datetime
import json

# Load tracked_data from a JSON file
def load_tracked_data():
    try:
        with open('tracked_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Tracked data file not found, starting with empty data.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return {}

# Save tracked_data to a JSON file
def save_tracked_data():
    try:
        with open('tracked_data.json', 'w') as file:
            json.dump(tracked_data, file, indent=4)
    except IOError as e:
        print(f"Error saving tracked data: {e}")

# Store prices for different symbols
tracked_data = load_tracked_data()

## Variables
on = True
refresh_interval = 900  # Default to 15 minutes

# Create the main window
root = tk.Tk()
root.title("Stock Tracker")

# Widget storage
name_labels = []
symbol_labels = []
color_boxes = []
price_entries = []
nownow_prices = []
lowtarget_entries = []
hightarget_entries = []

def set_lowtarget(symbol, new_lowtarget):
    try:
        new_lowtarget = float(new_lowtarget)
        if symbol in tracked_data:
            tracked_data[symbol]['lowtarget'] = new_lowtarget
            print(f"Success: Updated target {tracked_data[symbol]['name']} to {new_lowtarget}")
        else:
            print(f"Error: Symbol {symbol} not found!")
    except ValueError:
        print("Error: Please enter a valid number for the low target.")

def set_hightarget(symbol, new_hightarget):
    try:
        new_hightarget = float(new_hightarget)
        if symbol in tracked_data:
            tracked_data[symbol]['hightarget'] = new_hightarget
            print(f"Success: Updated target {tracked_data[symbol]['name']} to {new_hightarget}")
        else:
            print(f"Error: Symbol {symbol} not found!")
    except ValueError:
        print("Error: Please enter a valid number for the high target.")

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

def fetch_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.fast_info.last_price
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def nowround(symbol):
    data = fetch_price(symbol)
    if data is not None:
        return round(data, 4)
    return None

def lasttime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

def color(symbol):
    current_price = fetch_price(symbol)
    if current_price is None:
        return "gray"  # Gray if there's an issue fetching the price
    if current_price > tracked_data[symbol]['hightarget']:
        return "purple"
    elif current_price > tracked_data[symbol]['lowtarget']:
        return "blue"
    elif current_price > tracked_data[symbol]['price']:
        return "green"
    else:
        return "red"

def update_data():
    for i, symbol in enumerate(tracked_data.keys()):
        new_price = float(price_entries[i].get())
        new_lowtarget = float(lowtarget_entries[i].get())
        new_hightarget = float(hightarget_entries[i].get())
        tracked_data[symbol]['price'] = new_price
        tracked_data[symbol]['lowtarget'] = new_lowtarget
        tracked_data[symbol]['hightarget'] = new_hightarget
    save_tracked_data()

class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        tk.Label(root, text='Bought at:').grid(row=0, column=3)
        tk.Label(root, text='Current Price: ').grid(row=0, column=4)
        tk.Label(root, text='High Target: ').grid(row=0, column=5)
        tk.Label(root, text='Low Target: ').grid(row=0, column=6)

        self.time_label = tk.Label(root, text=lasttime())
        self.time_label.grid(row=0, column=0, columnspan=3)

        for i, symbol in enumerate(tracked_data.keys(), start=1):
            self.create_symbol_row(i, symbol, tracked_data[symbol])

        # Add a refresh button
        refresh_button = tk.Button(root, text="Refresh", command=self.refresh)
        refresh_button.grid(row=len(tracked_data) + 1, column=5, columnspan=1)

        # Add an update button to save changes
        add_button = tk.Button(root, text="Add", command=update_data)
        add_button.grid(row=len(tracked_data) + 1, column=6, columnspan=1)

        # Add an exit button
        exit_button = tk.Button(root, text="Exit", command=self.stop_program)
        exit_button.grid(row=len(tracked_data)+1, column=1, columnspan=1)

        self.refresh()

    def create_symbol_row(self, i, symbol, data):
        tk.Label(root, text=data['name']).grid(row=i, column=0)
        tk.Label(root, text=symbol).grid(row=i, column=1)
        color_box = tk.Label(root, width=10, height=2, relief="solid")
        color_box.grid(row=i, column=2)

        price_entry = tk.Entry(root)
        price_entry.grid(row=i, column=3)
        price_entry.insert(0, data['price'])
        price_entries.append(price_entry)

        now_price = tk.Label(root, text=nowround(symbol))
        now_price.grid(row=i, column=4)
        nownow_prices.append(now_price)

        hightarget_entry = tk.Entry(root)
        hightarget_entry.grid(row=i, column=5)
        hightarget_entry.insert(0, data['hightarget'])
        hightarget_entries.append(hightarget_entry)

        lowtarget_entry = tk.Entry(root)
        lowtarget_entry.grid(row=i, column=6)
        lowtarget_entry.insert(0, data['lowtarget'])
        lowtarget_entries.append(lowtarget_entry)

        name_labels.append(tk.Label(root))
        symbol_labels.append(tk.Label(root))
        color_boxes.append(color_box)

    def refresh(self):
        global on
        if on:
            for symbol in tracked_data.keys():
                tracked_data[symbol]['color'] = color(symbol)
                tracked_data[symbol]['nownow'] = nowround(symbol)
            self.update_gui()
            Timer(refresh_interval, self.refresh).start()  # Use configurable interval

    def update_gui(self):
        self.time_label.config(text=lasttime())
        for i, symbol in enumerate(tracked_data.keys()):
            data = tracked_data[symbol]
            set_price(symbol, price_entries[i].get())
            set_hightarget(symbol, hightarget_entries[i].get())
            set_lowtarget(symbol, lowtarget_entries[i].get())

            nownow_prices[i].config(text=data['nownow'])
            color_boxes[i].config(bg=data['color'])

    def stop_program(self):
        global on
        on = False
        self.master.destroy()
        exit()

# Go, be free
app = App(master=root)
root.mainloop()

