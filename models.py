from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "mysql+pymysql://root:GassyPenguin16@localhost:3306/inventory_management"

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
def seed_roles(session):
    existing_roles = session.query(Role).all()
    existing_role_names = {role.role for role in existing_roles}
    roles_to_add = ["Manager", "Sales", "Customer"]
    
    for role_name in roles_to_add:
        if role_name not in existing_role_names:
            role = Role(role=role_name)
            session.add(role)
    session.commit()

# Seed roles
session = SessionLocal()
seed_roles(session)
session.close()
