from models import Transaction, ItemizedTransaction


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
        # Create a new transaction
        new_transaction = Transaction(
            customer_id=customer_id,
            employee_id=employee_id,
            transaction_date=transaction_date,
            rental_date=rental_date,
            return_date=return_date,
        )
        session.add(new_transaction)
        session.flush()  # Ensure new_transaction.id is available

        # Add itemized transactions
        for item_id, quantity in inventory_items:
            for _ in range(quantity):  # Add multiple entries based on quantity
                itemized_transaction = ItemizedTransaction(
                    transaction_id=new_transaction.id, inventory_id=item_id
                )
                session.add(itemized_transaction)

        session.commit()
        print(f"Transaction added successfully with ID {new_transaction.id}.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add transaction: {e}")
