from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role

DATABASE_URL = "mysql+pymysql://root:GassyPenguin16@localhost:3306/inventory_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_user(name, last, email, role_name):
    session = SessionLocal()
    try:
        # Get the role object
        role = session.query(Role).filter_by(role=role_name).first()
        if not role:
            print(f"Role '{role_name}' does not exist.")
            return

        # Create a new user
        new_user = User(name=name, last=last, email=email, role_id=role.id)
        session.add(new_user)
        session.commit()
        print(f"User {name} {last} added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add user: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    name = input("Enter first name: ")
    last = input("Enter last name: ")
    email = input("Enter email: ")
    role_name = input("Enter role (Manager, Sales, Customer): ")
    add_user(name, last, email, role_name)
