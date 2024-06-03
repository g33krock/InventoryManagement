"""
Author: Collin Maassen, with assistance from my friends Dallas Lovell and Will Baird

Course: CSE 111

Professor Lindstrom

Date: 06/05/2024

"""

from models import Inventory


def add_inventory_item(session):
    name = input("Enter item name: ")
    price = float(input("Enter item price: "))
    rental = float(input("Enter item rental price: "))
    description = input("Enter item description: ")

    try:
        new_item = Inventory(
            name=name, price=price, rental=rental, description=description
        )
        session.add(new_item)
        session.commit()
        print(f"Inventory item '{name}' added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add inventory item: {e}")
