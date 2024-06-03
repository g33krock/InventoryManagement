"""
Author: Collin Maassen, with assistance from my friends Dallas Lovell and Will Baird

Course: CSE 111

Professor Lindstrom

Date: 06/05/2024

"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from add_user import add_user
from add_inventory import add_inventory_item
from add_transaction import add_transaction
from dotenv import load_dotenv # type: ignore

load_dotenv()

DATABASE_URL = f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/inventory_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    session = SessionLocal()
    while True:
        print("\nSelect an option:")
        print("1. Add User")
        print("2. Add Inventory Item")
        print("3. Add Transaction")
        print("4. Exit")

        try:
            choice = int(input("Enter choice: "))
            if choice == 1:
                add_user(session)
            elif choice == 2:
                add_inventory_item(session)
            elif choice == 3:
                add_transaction_interface(session)
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    session.close()

def add_transaction_interface(session):
    from datetime import datetime
    from models import User, Inventory

    # Select customers and employees for selection
    customers = session.query(User).filter_by(role_id=3).all()  # role_id 3 is for Customers
    employees = session.query(User).filter(User.role_id != 3).all()  # other role_ids are for employees

    # Display customers
    print("Available customers:")
    for idx, customer in enumerate(customers):
        print(f"{idx + 1}. {customer.name} {customer.last} (ID: {customer.id})")

    # Select customer
    while True:
        try:
            customer_index = int(input("Select customer by number: ")) - 1
            if customer_index < 0 or customer_index >= len(customers):
                raise IndexError
            selected_customer = customers[customer_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please select a valid customer number.")

    # Display employees
    print("Available employees:")
    for idx, employee in enumerate(employees):
        print(f"{idx + 1}. {employee.name} {employee.last} (ID: {employee.id})")

    # Select employee
    while True:
        try:
            employee_index = int(input("Select employee by number: ")) - 1
            if employee_index < 0 or employee_index >= len(employees):
                raise IndexError
            selected_employee = employees[employee_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please select a valid employee number.")

    # Display inventory items
    inventory_items = session.query(Inventory).all()
    print("Available inventory items:")
    for idx, item in enumerate(inventory_items):
        print(f"{idx + 1}. {item.name} (ID: {item.id}) - Price: {item.price}, Rental: {item.rental}")

    # Select inventory items with quantities
    selected_items = []
    while True:
        try:
            item_entries = input("Enter inventory item numbers and quantities (comma separated, e.g., 1:2,2:1): ").split(',')
            for entry in item_entries:
                item_index, quantity = entry.split(':')
                item_index = int(item_index.strip()) - 1
                quantity = int(quantity.strip())
                if item_index < 0 or item_index >= len(inventory_items):
                    raise IndexError
                selected_items.append((inventory_items[item_index].id, quantity))
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please enter valid inventory item numbers and quantities.")

    # Input transaction dates
    transaction_date = datetime.strptime(input("Enter transaction date (YYYY-MM-DD): "), "%Y-%m-%d").date()
    rental_date = datetime.strptime(input("Enter rental date (YYYY-MM-DD): "), "%Y-%m-%d").date()
    return_date = datetime.strptime(input("Enter return date (YYYY-MM-DD): "), "%Y-%m-%d").date()

    # Add transaction
    add_transaction(
        customer_id=selected_customer.id,
        employee_id=selected_employee.id,
        inventory_items=selected_items,
        transaction_date=transaction_date,
        rental_date=rental_date,
        return_date=return_date,
        session=session
    )


if __name__ == "__main__":
    main()
