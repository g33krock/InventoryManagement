from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Inventory, Transaction, ItemizedTransaction
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:GassyPenguin16@localhost:3306/inventory_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_transaction(customer_id, employee_id, inventory_items, transaction_date, rental_date, return_date):
    session = SessionLocal()
    try:
        # Create a new transaction
        new_transaction = Transaction(
            customer_id=customer_id,
            employee_id=employee_id,
            transaction_date=transaction_date,
            rental_date=rental_date,
            return_date=return_date
        )
        session.add(new_transaction)
        session.flush()  # Ensure new_transaction.id is available

        # Add itemized transactions
        for item_id in inventory_items:
            itemized_transaction = ItemizedTransaction(
                transaction_id=new_transaction.id,
                inventory_id=item_id
            )
            session.add(itemized_transaction)

        session.commit()
        print(f"Transaction added successfully with ID {new_transaction.id}.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add transaction: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    session = SessionLocal()

    # Fetch customers and employees for selection
    customers = session.query(User).filter_by(role_id=3).all()
    employees = session.query(User).filter(User.role_id != 3).all()

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

    # Select inventory items
    selected_items = []
    while True:
        try:
            item_indices = input("Enter inventory item numbers (comma separated): ").split(',')
            for item_index in item_indices:
                item_index = int(item_index.strip()) - 1
                if item_index < 0 or item_index >= len(inventory_items):
                    raise IndexError
                selected_items.append(inventory_items[item_index].id)
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please select valid inventory item numbers.")

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
        return_date=return_date
    )

    session.close()
