from datetime import datetime
from models import Transaction, ItemizedTransaction, Inventory, User

def add_transaction(
    customer_id,
    employee_id,
    inventory_items,
    transaction_date,
    rental_date,
    return_date,
    session,
):
    try:
        rental_days = (return_date - rental_date).days

        new_transaction = Transaction(
            customer_id=customer_id,
            employee_id=employee_id,
            transaction_date=transaction_date,
            rental_date=rental_date,
            return_date=return_date,
        )
        session.add(new_transaction)
        session.flush()

        total_cost = 0.0

        for item_id, quantity in inventory_items:
            inventory_item = session.query(Inventory).filter_by(id=item_id).first()
            if not inventory_item:
                raise ValueError(f"Inventory item with ID {item_id} not found.")
            
            unit_cost = inventory_item.rental * rental_days * quantity
            total_cost += unit_cost
            
            for _ in range(quantity):
                itemized_transaction = ItemizedTransaction(
                    transaction_id=new_transaction.id, inventory_id=item_id
                )
                session.add(itemized_transaction)

        session.commit()
        print(f"Transaction added successfully with ID {new_transaction.id}.")
        print_receipt(customer_id, employee_id, inventory_items, rental_days, total_cost, session)

    except Exception as e:
        session.rollback()
        print(f"Failed to add transaction: {e}")

def print_receipt(customer_id, employee_id, inventory_items, rental_days, total_cost, session):
    customer = session.query(User).filter_by(id=customer_id).first()
    employee = session.query(User).filter_by(id=employee_id).first()

    print("\n----- Transaction Receipt -----")
    print(f"Customer: {customer.name} {customer.last}")
    print(f"Employee: {employee.name} {employee.last}")
    print(f"Rental Days: {rental_days}")
    print("Items Rented:")

    for item_id, quantity in inventory_items:
        inventory_item = session.query(Inventory).filter_by(id=item_id).first()
        if inventory_item:
            print(f"- {inventory_item.name}: {quantity} units @ {inventory_item.rental} per day")

    print(f"Total Cost: ${total_cost:.2f}")
    print("-------------------------------\n")
