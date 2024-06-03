import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the root project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, ItemizedTransaction, Transaction, Inventory, User, Role

# Configure the test database URL
TEST_DATABASE_URL = "sqlite:///./test_inventory_management.db"

@pytest.fixture(scope='module')
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='module')
def test_session(test_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(autouse=True)
def clear_data(test_session):
    # Clear data before each test
    test_session.query(ItemizedTransaction).delete()
    test_session.query(Transaction).delete()
    test_session.query(Inventory).delete()
    test_session.query(User).delete()
    test_session.query(Role).delete()
    test_session.commit()
