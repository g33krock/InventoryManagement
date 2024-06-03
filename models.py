"""
Author: Collin Maassen, with assistance from my friends Dallas Lovell and Will Baird

Course: CSE 111

Professor Lindstrom

Date: 06/05/2024

"""
import os
from dotenv import load_dotenv # type: ignore
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

load_dotenv()

DATABASE_URL = f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/inventory_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=False, index=True)
    last = Column(String(50), unique=False, index=True)
    email = Column(String(120), unique=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship("Role", back_populates="users")

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), unique=False, index=True)

    users = relationship("User", back_populates="role")

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=False, index=True)
    price = Column(Float, unique=False, index=True)
    rental = Column(Float, unique=False, index=True)
    description = Column(String(120), unique=False, index=True)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    transaction_date = Column(Date, index=True)
    rental_date = Column(Date, index=True)
    return_date = Column(Date, index=True)

    customer = relationship("User", foreign_keys=[customer_id], backref="customer_transactions")
    employee = relationship("User", foreign_keys=[employee_id], backref="employee_transactions")

class ItemizedTransaction(Base):
    __tablename__ = 'itemized_transactions'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventory.id'), nullable=False)

    transaction = relationship("Transaction", backref="itemized_transactions")
    inventory = relationship("Inventory", backref="itemized_transactions")

# Create tables
Base.metadata.create_all(bind=engine)

# Seed script
def clear_data(session):
    # Clear all data from the tables
    session.query(ItemizedTransaction).delete()
    session.query(Transaction).delete()
    session.query(Inventory).delete()
    session.query(User).delete()
    session.query(Role).delete()
    session.commit()

    # Reset auto-increment counters
    session.execute(text('ALTER TABLE itemized_transactions AUTO_INCREMENT = 1'))
    session.execute(text('ALTER TABLE transactions AUTO_INCREMENT = 1'))
    session.execute(text('ALTER TABLE inventory AUTO_INCREMENT = 1'))
    session.execute(text('ALTER TABLE users AUTO_INCREMENT = 1'))
    session.execute(text('ALTER TABLE roles AUTO_INCREMENT = 1'))
    session.commit()

def seed_roles(session):
    roles_to_add = ["Manager", "Sales", "Customer"]
    
    for role_name in roles_to_add:
        role = Role(role=role_name)
        session.add(role)
    session.commit()

def seed_users(session):
    users_to_add = [
        {"name": "Alice", "last": "Smith", "email": "alice@example.com", "role_name": "Manager"},
        {"name": "Bob", "last": "Johnson", "email": "bob@example.com", "role_name": "Sales"},
        {"name": "Sharon", "last": "Kline", "email": "sharon@example.com", "role_name": "Sales"},
        {"name": "Charlie", "last": "Lee", "email": "charlie@example.com", "role_name": "Customer"},
        {"name": "Abby", "last": "Deer", "email": "abby@example.com", "role_name": "Customer"},
        {"name": "Jorje", "last": "Rodriguez", "email": "jorje@example.com", "role_name": "Customer"}
    ]
    for user in users_to_add:
        role = session.query(Role).filter_by(role=user["role_name"]).first()
        new_user = User(name=user["name"], last=user["last"], email=user["email"], role_id=role.id)
        session.add(new_user)
    session.commit()

def seed_inventory(session):
    inventory_to_add = [
        {"name": "Single Tube", "price": 10.0, "rental": 2.0, "description": "River tube for a single rider"},
        {"name": "Double Tube", "price": 20.0, "rental": 3.0, "description": "River tube for 2 riders"},
        {"name": "Double Cooler Tube", "price": 30.0, "rental": 4.0, "description": "River tube for 2 rides with an embedded cooler"}
    ]
    for item in inventory_to_add:
        new_item = Inventory(name=item["name"], price=item["price"], rental=item["rental"], description=item["description"])
        session.add(new_item)
    session.commit()

# Clear existing data and seed new data
session = SessionLocal()
clear_data(session)
seed_roles(session)
seed_users(session)
seed_inventory(session)
session.close()
