import yfinance as yf
from threading import Timer
import tkinter as tk
from datetime import datetime
import json

from lxml.objectify import NoneElement


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
        print(f"Debug: Fetching price for {symbol} failed, setting color to gray.")
        return "gray"  # Gray if there's an issue fetching the price

    # Get targets from tracked data
    try:
        data = tracked_data[symbol]
        if current_price > data['hightarget']:
            return "purple"
        elif current_price > data['lowtarget']:
            return "blue"
        elif current_price > data['price']:
            return "green"
        else:
            return "red"
    except KeyError:
        print(f"Debug: Symbol {symbol} not found in tracked_data!")
        return "gray"  # Default to gray if the symbol is not found


def update_widgets(self):
    self.time_label.config(text=lasttime())
    for i, symbol in enumerate(tracked_data.keys()):
        data = tracked_data[symbol]
        try:
            price_entries[i].insert(0, data['price'])
            lowtarget_entries[i].insert(0, data['lowtarget'])
            hightarget_entries[i].insert(0, data['hightarget'])
        except IndexError:
            print(f"Debug: IndexError at {i} for symbol {symbol}")

        # Update color and current price
        new_color = color(symbol)
        color_boxes[i].config(bg=new_color)
        nownow_prices[i].config(text=nowround(symbol))



class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        tk.Label(root, text='Bought at:').grid(row=0, column=3)
        tk.Label(root, text='Current Price: ').grid(row=0, column=4)
        tk.Label(root, text='High Target: ').grid(row=0, column=5)
        tk.Label(root, text='Low Target: ').grid(row=0, column=6)

        self.time_label = tk.Label(root, text=lasttime())
        self.time_label.grid(row=0, column=0, columnspan=3)

        self.update_widgets()

        # Add a refresh button
        refresh_button = tk.Button(root, text="Refresh", command=self.refresh)
        refresh_button.grid(row=len(tracked_data) + 1, column=5, columnspan=1)

        # Add an update button to save changes
        add_button = tk.Button(root, text="Add", command=self.show_add_panel)
        add_button.grid(row=len(tracked_data) + 1, column=4, columnspan=1)

        # Add an exit button
        exit_button = tk.Button(root, text="Exit", command=self.stop_program)
        exit_button.grid(row=len(tracked_data) + 1, column=1, columnspan=1)

        self.refresh()

    def update_widgets(self):
        for widget in name_labels:
            widget.destroy()
        for widget in symbol_labels:
            widget.destroy()
        for widget in color_boxes:
            widget.destroy()
        for widget in price_entries:
            widget.destroy()
        for widget in nownow_prices:
            widget.destroy()
        for widget in lowtarget_entries:
            widget.destroy()
        for widget in hightarget_entries:
            widget.destroy()

        name_labels.clear()
        symbol_labels.clear()
        color_boxes.clear()
        price_entries.clear()
        nownow_prices.clear()
        lowtarget_entries.clear()
        hightarget_entries.clear()

        for i, symbol in enumerate(tracked_data.keys(), start=1):
            self.create_symbol_row(i, symbol, tracked_data[symbol])

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

    def show_add_panel(self):
        # Create a new top-level window
        add_window = tk.Toplevel(root)
        add_window.title("Add New Stock")

        tk.Label(add_window, text="Symbol:").grid(row=0, column=0)
        symbol_entry = tk.Entry(add_window)
        symbol_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Price:").grid(row=2, column=0)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Low Target:").grid(row=3, column=0)
        lowtarget_entry = tk.Entry(add_window)
        lowtarget_entry.grid(row=3, column=1)

        tk.Label(add_window, text="High Target:").grid(row=4, column=0)
        hightarget_entry = tk.Entry(add_window)
        hightarget_entry.grid(row=4, column=1)

        def update_and_close():
            symbol = symbol_entry.get().strip()
            if symbol in tracked_data:
                print(f"Error: Symbol {symbol} already exists!")
                return

            name = name_entry.get().strip()
            price = price_entry.get().strip()
            lowtarget = lowtarget_entry.get().strip()
            hightarget = hightarget_entry.get().strip()

            # Validate entries
            try:
                float(price)
                float(lowtarget)
                float(hightarget)
                float(fetch_price(symbol))
            except ValueError:
                print("Error: Please enter valid numbers for price, low target, high target, and current price.")
                return

            # Update tracked_data
            tracked_data[symbol] = {
                'name': name,
                'price': float(price),
                'lowtarget': float(lowtarget),
                'hightarget': float(hightarget),
                'color': color(symbol),  # Ensure symbol exists in tracked_data
                'nownow': nowround(symbol)
            }

            # Save the updated data
            save_tracked_data()

            # Close the add window
            add_window.destroy()

            # Refresh the main window
            self.update_widgets()

        update_button = tk.Button(add_window, text="Update", command=update_and_close)
        update_button.grid(row=5, column=1)

    def refresh(self):
        # Update GUI with new data
        self.update_widgets()
        for i, symbol in enumerate(tracked_data.keys()):
            color_boxes[i].config(bg=color(symbol))
            nownow_prices[i].config(text=nowround(symbol))

        # Schedule next update
        self.schedule_update()

    def stop_program(self):
        global on
        on = False
        root.quit()

    def schedule_update(self):
        if on:
            Timer(refresh_interval, self.refresh).start()


app = App(root)
root.mainloop()
