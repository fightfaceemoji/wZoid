import yfinance as yf
from yfinance import Ticker
import time
from threading import Timer
import tkinter as tk

# Store prices for different symbols
tracked_data = {
    'TSLA': {'name': 'Tesla', 'price': 221.1, 'target': 225},
    '^GSPC': {'name': 'S&P 500', 'price': 5597.12, 'target': 5650},
    'EUR=X': {'name': 'USD to EUR', 'price': 0.8988, 'target': 0.95},
    'BRK-B': {'name': 'Berkshire B', 'price': 448.00, 'target': 455},
    'AAPL': {'name': 'Apple', 'price': 226.51, 'target': 230}
}

##variables
on = True

# Create the main window
root = tk.Tk()
root.title("Stock Tracker")

# widget storage
name_labels = []
symbol_labels = []
color_boxes = []
price_entries = []
target_entries = []


def set_target(symbol, new_target):
    try:
        new_target = float(new_target)
        if symbol in tracked_data:
            tracked_data[symbol]['target'] = new_target
            print(f"Success: Updated target {tracked_data[symbol]['name']} to {new_target}")
        else:
            print(f"Error: Symbol {symbol} not found!")
    except ValueError:
        print("Error: Please enter a valid number for the target.")


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


def nownow(symbol):
#takes the most recent prices
    ticker = yf.Ticker(symbol)
    data = ticker.fast_info.last_price
    # print(data)
    return data


def color(symbol):
    # color code based on comparison
    current_price = nownow(symbol)
    if current_price > tracked_data[symbol]['target']:
        return "purple"
    elif current_price > tracked_data[symbol]['price']:
        return "green"
    else:
        return "red"



class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        tk.Label(root, text='Bought at:').grid(row=0, column=3)
        tk.Label(root, text='Sell Target: ').grid(row=0, column=4)

        for i, symbol in enumerate(tracked_data.keys(), start=1):
            ## CREATE LABEL BOXES
            tk.Label(root, text=tracked_data[symbol]['name']).grid(row=i, column=0)
            tk.Label(root, text=symbol).grid(row=i, column=1)
            color_box = tk.Label(root, width=10, height=2, relief="solid")
            color_box.grid(row=i, column=2)

            # Create an Entry widget and store it in the list
            price_entry = tk.Entry(root)
            price_entry.grid(row=i, column=3)
            price_entry.insert(0, tracked_data[symbol]['price'])
            price_entries.append(price_entry)

            target_entry = tk.Entry(root)
            target_entry.grid(row=i, column=4)
            target_entry.insert(0, tracked_data[symbol]['target'])
            target_entries.append(target_entry)

            name_labels.append(tk.Label(root))
            symbol_labels.append(tk.Label(root))
            color_boxes.append(color_box)

        # Add a button to exit the program
        exit_button = tk.Button(root, text="Exit", command=self.stop_program)
        exit_button.grid(row=len(tracked_data) + 1, column=1)
        refresh_button = tk.Button(root, text="Refresh", command=self.fresh_gui)
        refresh_button.grid(row=len(tracked_data) + 1, column=3, columnspan=2)

        self.fresh_gui()  # Initial call to populate colors based on initial prices

    ##SUPER IMPORTANT--- has color update
    def refresh(self):
        global on
        if on:
            for symbol in tracked_data.keys():
                # Update color based on current price
                tracked_data[symbol]['color'] = color(symbol)

    def fresh_gui(self):
        self.refresh()
        # Refresh the data and update the GUI elements
        for i, symbol in enumerate(tracked_data.keys()):
            set_price(symbol, price_entries[i].get())
            set_target(symbol, target_entries[i].get())  # Corrected here to use target_entries
            data = tracked_data[symbol]
            name_label = name_labels[i]
            symbol_label = symbol_labels[i]
            color_box = color_boxes[i]
            name_label.config(text=data['name'])
            symbol_label.config(text=symbol)
            color_box.config(bg=data['color'])

        Timer(10, self.fresh_gui).start()  # Continue refreshing every 10 seconds

    def stop_program(self):
        global on
        on = False
        self.master.destroy()
        exit()


##go, be free
app = App(master=root)
root.mainloop()
