# Alex Burns - Student Number: 100885375
# TPRG II Project 1
# November 15th, 2023

# Code was taken from ChatGPT on November 14th, 2023. Prompted by sending incomplete code and saying "Complete code that allows the GUI to act as a vending machine. The machine accepts nickels (5 cents), dimes (10 cents), quarters (25 cents), loonies (100 cents), and toonies (200 cents). The machine has 5 selections: surprise (150 cents), pop (100 cents), chips (125 cents), chocolate (150 cents), and beer (175 cents). The GUI tells you the total amount of coins put in. It will also calculate the change owed and dispense it. There is a return button that will return all coins to you." 
import PySimpleGUI as sg

# Constants for testing and logging
TESTING = True

def log(s):
    """Log the message if testing mode is enabled."""
    if TESTING:
        print(s)

class VendingMachine:
    """A state machine simulating a vending machine."""
    
    # Full list of products with their names and prices in cents
    PRODUCTS = {
        "surprise": ("SURPRISE", 150),
        "pop": ("POP", 100),
        "chips": ("CHIPS", 125),
        "choc": ("CHOCOLATE", 150),
        "beer": ("BEER", 175),
    }
    
    # Full list of coins and their values in cents
    COINS = {
        "5": ("NICKEL", 5),
        "10": ("DIME", 10),
        "25": ("QUARTER", 25),
        "100": ("LOONIE", 100),
        "200": ("TOONIE", 200),
    }
    
    def __init__(self):
        self.state = None
        self.states = {}
        self.event = ""
        self.amount = 0
        self.change_due = 0
        self.coin_values = sorted([value for (coin, value) in self.COINS.values()], reverse=True)
        log(f"Coin values: {self.coin_values}")
        
    def add_state(self, state):
        self.states[state.name] = state
    
    def go_to_state(self, state_name):
        if self.state:
            log(f'Exiting {self.state.name}')
            self.state.on_exit(self)
        self.state = self.states[state_name]
        log(f'Entering {self.state.name}')
        self.state.on_entry(self)
    
    def update(self):
        if self.state:
            self.state.update(self)
    
    def add_coin(self, coin):
        """Look up the value of the coin given by the key and add it."""
        self.amount += self.COINS[coin][1]
        log(f"Amount inserted: {self.amount}")
    
    def button_action(self):
        """Callback function for the button press."""
        self.event = 'RETURN'
        self.update()

# Define the states of the vending machine

class State:
    """Superclass for states, representing a state in the state machine."""
    _NAME = ""
    
    @property
    def name(self):
        return self._NAME
    
    def on_entry(self, machine):
        pass
    
    def on_exit(self, machine):
        pass
    
    def update(self, machine):
        pass

class WaitingState(State):
    _NAME = "waiting"
    
    def update(self, machine):
        if machine.event in machine.COINS:
            machine.add_coin(machine.event)
            machine.go_to_state('add_coins')

class AddCoinsState(State):
    _NAME = "add_coins"
    
    def update(self, machine):
        if machine.event == "RETURN":
            machine.change_due = machine.amount
            machine.amount = 0
            machine.go_to_state('count_change')
        elif machine.event in machine.COINS:
            machine.add_coin(machine.event)
        elif machine.event in machine.PRODUCTS:
            if machine.amount >= machine.PRODUCTS[machine.event][1]:
                machine.event = machine.event  # Set the event to the selected product
                machine.go_to_state('deliver_product')

class DeliverProductState(State):
    _NAME = "deliver_product"
    
    def on_entry(self, machine):
        product_name, product_price = machine.PRODUCTS[machine.event]
        machine.change_due = machine.amount - product_price
        machine.amount = 0
        machine.go_to_state('count_change')  # Proceed to count the change

class CountChangeState(State):
    _NAME = "count_change"
    
    def on_entry(self, machine):
        total_change_cents = 0  # Initialize the total change amount in cents
        change_returned = []
        for value, (coin, _) in sorted(machine.COINS.items(), key=lambda x: x[1][1], reverse=True):
            value = int(value)  # Convert value to an integer
            while machine.change_due >= value:
                machine.change_due -= value
                total_change_cents += value  # Add the coin value to the total change amount
                change_returned.append(coin)
        
        if total_change_cents > 0:
            machine.response = f"Change returned: {total_change_cents} cents ({', '.join(change_returned)})"
        else:
            machine.response = "No change to return"
        
        machine.go_to_state('waiting')  # Return to the waiting state after returning change

# MAIN PROGRAM
if __name__ == "__main__":
    sg.theme('BluePurple')
    
    response_area = sg.Multiline(default_text='', size=(35, 5), key='-OUTPUT-', autoscroll=True, echo_stdout_stderr=True, disabled=True)
    amount_display = sg.Text('Amount inserted: $0.00', key='-AMOUNT-', size=(35, 1))

    coin_col = [[sg.Text("ENTER COINS", font=("Helvetica", 24))]]
    for coin, (label, value) in VendingMachine.COINS.items():
        coin_col.append([sg.Button(label, font=("Helvetica", 18), key=coin)])

    select_col = [[sg.Text("SELECT ITEM", font=("Helvetica", 24))]]
    for product, (label, price) in VendingMachine.PRODUCTS.items():
        select_col.append([sg.Text(f"{label} - ${price / 100:.2f}", font=("Helvetica", 18)), sg.Button('Select', font=("Helvetica", 18), key=product)])

    layout = [
        [sg.Column(coin_col, vertical_alignment="top"), sg.VSeparator(), sg.Column(select_col, vertical_alignment="top")],
        [sg.Button("RETURN", font=("Helvetica", 12))],
        [amount_display],
        [response_area]
    ]
    
    window = sg.Window('Vending Machine', layout, finalize=True)
    vending = VendingMachine()
    vending.response = ""  # To store the response messages
    
    vending.add_state(WaitingState())
    vending.add_state(AddCoinsState())
    vending.add_state(DeliverProductState())
    vending.add_state(CountChangeState())

    vending.go_to_state('waiting')
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event:
            vending.event = event
            vending.update()
            window['-AMOUNT-'].update(f"Amount inserted: ${vending.amount / 100:.2f}")
            response_area.update(vending.response + "\n")
            vending.response = ""  # Reset the response message after updating the display

    window.close()
    print("Normal exit")
# Code was taken from ChatGPT on November 14th, 2023. Prompted by sending incomplete code and saying "Complete code that allows the GUI to act as a vending machine. The machine accepts nickels (5 cents), dimes (10 cents), quarters (25 cents), loonies (100 cents), and toonies (200 cents). The machine has 5 selections: surprise (150 cents), pop (100 cents), chips (125 cents), chocolate (150 cents), and beer (175 cents). The GUI tells you the total amount of coins put in. It will also calculate the change owed and dispense it. There is a return button that will return all coins to you."