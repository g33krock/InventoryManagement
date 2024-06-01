from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Inventory

DATABASE_URL = "mysql+pymysql://root:GassyPenguin16@localhost:3306/inventory_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_inventory_item(name, price, rental, description):
    session = SessionLocal()
    try:
        new_item = Inventory(name=name, price=price, rental=rental, description=description)
        session.add(new_item)
        session.commit()
        print(f"Inventory item '{name}' added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add inventory item: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    name = input("Enter item name: ")
    price = float(input("Enter item price: "))
    rental = float(input("Enter item rental price: "))
    description = input("Enter item description: ")
    
    add_inventory_item(name, price, rental, description)
