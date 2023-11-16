# Alex Burns - Student Number: 100885375
# TPRG II Project 1
# November 15th, 2023

# Code taken from ChatGPT on November 15th, 2023. Prompted by sending full code vending_machine and asking "Come up with 4 random PyTests for the following code."
import pytest
from vending_machine import VendingMachine, WaitingState, AddCoinsState, DeliverProductState, CountChangeState

@pytest.fixture
def vending():
    machine = VendingMachine()
    machine.add_state(WaitingState())
    machine.add_state(AddCoinsState())
    machine.add_state(DeliverProductState())
    machine.add_state(CountChangeState())
    machine.go_to_state('waiting')  # Set the initial state to 'waiting'
    return machine

def test_insert_quarter(vending):
    vending.event = '25'  # Simulate inserting a quarter
    vending.update()      # Trigger the update to change state
    assert vending.state.name == 'add_coins'
    assert vending.amount == 25

def test_insert_loonie(vending):
    vending.event = '100'  # Simulate inserting a loonie
    vending.update()       # Trigger the update to change state
    assert vending.state.name == 'add_coins'
    assert vending.amount == 100

def test_insert_toonie(vending):
    vending.event = '200'  # Simulate inserting a toonie
    vending.update()       # Trigger the update to change state
    assert vending.state.name == 'add_coins'
    assert vending.amount == 200

def test_multi_coin_insertion(vending):
    vending.event = '100'  # Simulate inserting a loonie
    vending.update()       # Trigger the update to change state
    vending.event = '200'  # Simulate inserting a toonie
    vending.update()       # Trigger the update to change state
    vending.event = '25'   # Simulate inserting a quarter
    vending.update()       # Trigger the update to change state
    assert vending.state.name == 'add_coins'
    assert vending.amount == 325
# Code taken from ChatGPT on November 15th, 2023. Prompted by sending full code vending_machine and asking "Come up with 4 random PyTests for the following code."