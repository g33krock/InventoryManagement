import pytest
from unittest.mock import patch
from add_user import add_user
from add_inventory import add_inventory_item
from add_transaction import add_transaction
from models import Role, User, Inventory, Transaction, ItemizedTransaction
from datetime import datetime

def test_add_user(test_session, monkeypatch):
    # Seed roles
    roles = ["Manager", "Sales", "Customer"]
    for role in roles:
        test_session.add(Role(role=role))
    test_session.commit()

    # Mock input for add_user function
    user_inputs = iter(['Alice', 'Smith', 'alice@example.com', '1'])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    add_user(test_session)

    # Verify user was added
    user = test_session.query(User).filter_by(email="alice@example.com").first()
    assert user is not None
    assert user.name == "Alice"
    assert user.last == "Smith"
    assert user.email == "alice@example.com"
    assert user.role.role == "Manager"

def test_add_inventory_item(test_session, monkeypatch):
    # Mock input for add_inventory_item function
    user_inputs = iter(['Single Tube', '10.0', '2.0', 'River tube for a single rider'])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    add_inventory_item(test_session)

    # Verify inventory item was added
    item = test_session.query(Inventory).filter_by(name="Single Tube").first()
    assert item is not None
    assert item.name == "Single Tube"
    assert item.price == 10.0
    assert item.rental == 2.0
    assert item.description == "River tube for a single rider"

def test_add_transaction(test_session):
    # Seed roles and users
    roles = ["Manager", "Sales", "Customer"]
    for role in roles:
        test_session.add(Role(role=role))
    test_session.commit()

    users = [
        {"name": "Alice", "last": "Smith", "email": "alice@example.com", "role_name": "Manager"},
        {"name": "Bob", "last": "Johnson", "email": "bob@example.com", "role_name": "Sales"},
        {"name": "Charlie", "last": "Lee", "email": "charlie@example.com", "role_name": "Customer"}
    ]
    for user in users:
        role = test_session.query(Role).filter_by(role=user["role_name"]).first()
        new_user = User(name=user["name"], last=user["last"], email=user["email"], role_id=role.id)
        test_session.add(new_user)
    test_session.commit()

    # Seed inventory items
    inventory_to_add = [
        {"name": "Single Tube", "price": 10.0, "rental": 2.0, "description": "River tube for a single rider"},
        {"name": "Double Tube", "price": 20.0, "rental": 3.0, "description": "River tube for 2 riders"}
    ]
    for item in inventory_to_add:
        new_item = Inventory(name=item["name"], price=item["price"], rental=item["rental"], description=item["description"])
        test_session.add(new_item)
    test_session.commit()

    # Add transaction
    customer = test_session.query(User).filter_by(email="charlie@example.com").first()
    employee = test_session.query(User).filter_by(email="alice@example.com").first()
    inventory_items = [(1, 1), (2, 2)]  # Add 1 Single Tube and 2 Double Tubes
    transaction_date = datetime.strptime("2023-05-01", "%Y-%m-%d").date()
    rental_date = datetime.strptime("2023-05-02", "%Y-%m-%d").date()
    return_date = datetime.strptime("2023-05-03", "%Y-%m-%d").date()

    add_transaction(customer.id, employee.id, inventory_items, transaction_date, rental_date, return_date, test_session)

    # Verify transaction was added
    transaction = test_session.query(Transaction).first()
    assert transaction is not None
    assert transaction.customer_id == customer.id
    assert transaction.employee_id == employee.id
    assert transaction.transaction_date == transaction_date
    assert transaction.rental_date == rental_date
    assert transaction.return_date == return_date

    # Verify itemized transactions
    itemized_transactions = test_session.query(ItemizedTransaction).all()
    assert len(itemized_transactions) == 3
    assert itemized_transactions[0].inventory_id == 1
    assert itemized_transactions[1].inventory_id == 2
    assert itemized_transactions[2].inventory_id == 2
