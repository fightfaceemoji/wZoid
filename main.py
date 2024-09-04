import yfinance as yf
from threading import Timer
import tkinter as tk

# Store prices for different symbols
tracked_data = {
    'TSLA': {'name': 'Tesla', 'price': 221.1, 'lowtarget': 225, 'hightarget': 230},
    '^GSPC': {'name': 'S&P 500', 'price': 5597.12, 'lowtarget': 5650, 'hightarget': 230},
    'EUR=X': {'name': 'USD to EUR', 'price': 0.8988, 'lowtarget': 0.95, 'hightarget': 230},
    'BRK-B': {'name': 'Berkshire B', 'price': 448.00, 'lowtarget': 455, 'hightarget': 230},
    'AAPL': {'name': 'Apple', 'price': 226.51, 'lowtarget': 230, 'hightarget': 230}
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


def nownow(symbol):
#takes the most recent prices
    ticker = yf.Ticker(symbol)
    data = ticker.fast_info.last_price
    # print(data)
    return data


def color(symbol):
    # color code based on comparison
    current_price = nownow(symbol)
    if current_price > tracked_data[symbol]['hightarget']:
        return "purple"
    elif current_price < tracked_data[symbol]['lowtarget']:
        return "blue"
    elif current_price > tracked_data[symbol]['price']:
        return "green"
    else:
        return "red"


def refresh():
    ##SUPER IMPORTANT--- has color update
    global on
    if on:
        for symbol in tracked_data.keys():
            # Update color based on current price
            tracked_data[symbol]['color'] = color(symbol)
            tracked_data[symbol]['nownow'] = nownow(symbol)

class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        tk.Label(root, text='Bought at:').grid(row=0, column=3)
        tk.Label(root, text='Current Price: ').grid(row=0, column=4)
        tk.Label(root, text='High Target: ').grid(row=0, column=5)
        tk.Label(root, text='Low Target: ').grid(row=0, column=6)

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

            nownow_price = (tk.Label(root, text=nownow(symbol)))
            nownow_price.grid(row=i, column=4)

            hightarget_entry = tk.Entry(root)
            hightarget_entry.grid(row=i, column=5)
            hightarget_entry.insert(0, tracked_data[symbol]['hightarget'])
            hightarget_entries.append(hightarget_entry)

            lowtarget_entry = tk.Entry(root)
            lowtarget_entry.grid(row=i, column=6)
            lowtarget_entry.insert(0, tracked_data[symbol]['lowtarget'])
            lowtarget_entries.append(lowtarget_entry)

            name_labels.append(tk.Label(root))
            symbol_labels.append(tk.Label(root))
            nownow_prices.append(nownow_price)
            color_boxes.append(color_box)

        # Add a button to exit the program
        exit_button = tk.Button(root, text="Exit", command=self.stop_program)
        exit_button.grid(row=len(tracked_data) + 1, column=1)
        refresh_button = tk.Button(root, text="Refresh", command=self.fresh_gui)
        refresh_button.grid(row=len(tracked_data) + 1, column=5, columnspan=2)

        self.fresh_gui()  # Initial call to populate colors based on initial prices

    def fresh_gui(self):
        refresh()
        # Refresh the data and update the GUI elements
        for i, symbol in enumerate(tracked_data.keys()):
            set_price(symbol, price_entries[i].get())
            set_hightarget(symbol, hightarget_entries[i].get())
            set_lowtarget(symbol, lowtarget_entries[i].get())  # Corrected here to use target_entries
            data = tracked_data[symbol]
            name_label = name_labels[i]
            symbol_label = symbol_labels[i]
            color_box = color_boxes[i]
            nownow_price = nownow_prices[i]

            name_label.config(text=data['name'])
            symbol_label.config(text=symbol)
            color_box.config(bg=data['color'])

        Timer(900, self.fresh_gui).start()  # Continue refreshing every 10 seconds

    def stop_program(self):
        global on
        on = False
        self.master.destroy()
        exit()


##go, be free
app = App(master=root)
root.mainloop()