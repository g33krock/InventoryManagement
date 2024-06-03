from models import Base, User, Role, Inventory, Transaction, ItemizedTransaction
from datetime import datetime

def test_models(test_session):
    # Test creating roles
    role = Role(role="Manager")
    test_session.add(role)
    test_session.commit()
    assert test_session.query(Role).count() == 1

    # Test creating users
    user = User(name="Test", last="User", email="test@example.com", role_id=role.id)
    test_session.add(user)
    test_session.commit()
    assert test_session.query(User).count() == 1
    assert user.role.role == "Manager"

    # Test creating inventory items
    item = Inventory(name="Test Item", price=10.0, rental=2.0, description="Test description")
    test_session.add(item)
    test_session.commit()
    assert test_session.query(Inventory).count() == 1

    # Test creating transactions
    transaction = Transaction(
        customer_id=user.id, 
        employee_id=user.id, 
        transaction_date=datetime.strptime("2023-05-01", "%Y-%m-%d").date(), 
        rental_date=datetime.strptime("2023-05-02", "%Y-%m-%d").date(), 
        return_date=datetime.strptime("2023-05-03", "%Y-%m-%d").date()
    )
    test_session.add(transaction)
    test_session.commit()
    assert test_session.query(Transaction).count() == 1

    # Test creating itemized transactions
    itemized_transaction = ItemizedTransaction(transaction_id=transaction.id, inventory_id=item.id)
    test_session.add(itemized_transaction)
    test_session.commit()
    assert test_session.query(ItemizedTransaction).count() == 1
