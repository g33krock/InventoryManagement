import pytest
from unittest.mock import patch
from main import main
from models import Role, User, Inventory, Transaction, ItemizedTransaction
from datetime import datetime

def test_main_add_user(test_session, monkeypatch):
    # Seed roles
    roles = ["Manager", "Sales", "Customer"]
    for role in roles:
        test_session.add(Role(role=role))
    test_session.commit()

    user_inputs = iter(['1', 'Alice', 'Smith', 'alice@example.com', '1', '4'])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    main()

    # Verify user was added
    user = test_session.query(User).filter_by(email="alice@example.com").first()
    assert user is not None
    assert user.name == "Alice"
    assert user.last == "Smith"
    assert user.email == "alice@example.com"
    assert user.role.role == "Manager"

def test_main_add_inventory(test_session, monkeypatch):
    user_inputs = iter(['2', 'Single Tube', '10.0', '2.0', 'River tube for a single rider', '4'])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    main()

    # Verify inventory item was added
    item = test_session.query(Inventory).filter_by(name="Single Tube").first()
    assert item is not None
    assert item.name == "Single Tube"
    assert item.price == 10.0
    assert item.rental == 2.0
    assert item.description == "River tube for a single rider"

def test_main_add_transaction(test_session, monkeypatch):
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

    user_inputs = iter([
        '3',  # Select "Add Transaction"
        '3',  # Select customer
        '1',  # Select employee
        '1:2,2:1',  # Select inventory items and quantities
        '2023-05-01',  # Transaction date
        '2023-05-02',  # Rental date
        '2023-05-03',  # Return date
        '4'  # Exit
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    main()

    # Verify transaction was added
    transaction = test_session.query(Transaction).first()
    assert transaction is not None
    customer = test_session.query(User).filter_by(email="charlie@example.com").first()
    employee = test_session.query(User).filter_by(email="alice@example.com").first()
    assert transaction.customer_id == customer.id
    assert transaction.employee_id == employee.id
    assert transaction.transaction_date == datetime.strptime("2023-05-01", "%Y-%m-%d").date()
    assert transaction.rental_date == datetime.strptime("2023-05-02", "%Y-%m-%d").date()
    assert transaction.return_date == datetime.strptime("2023-05-03", "%Y-%m-%d").date()

    # Verify itemized transactions
    itemized_transactions = test_session.query(ItemizedTransaction).all()
    assert len(itemized_transactions) == 3
    assert itemized_transactions[0].inventory_id == 1
    assert itemized_transactions[1].inventory_id == 2
    assert itemized_transactions[2].inventory_id == 2
