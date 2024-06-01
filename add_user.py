from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role

DATABASE_URL = "mysql+pymysql://root:GassyPenguin16@localhost:3306/inventory_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_roles(session):
    """Retrieve all roles from the database."""
    return session.query(Role).all()

def add_user(name, last, email, role_id):
    session = SessionLocal()
    try:
        # Create a new user
        new_user = User(name=name, last=last, email=email, role_id=role_id)
        session.add(new_user)
        session.commit()
        print(f"User {name} {last} added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add user: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    session = SessionLocal()
    
    # Fetch roles from the database
    roles = get_roles(session)
    
    # Display roles to the user
    print("Available roles:")
    for idx, role in enumerate(roles):
        print(f"{idx + 1}. {role.role}")
    
    # Prompt user for details
    name = input("Enter first name: ")
    last = input("Enter last name: ")
    email = input("Enter email: ")

    while True:
        try:
            role_index = int(input("Select role by number: ")) - 1
            if role_index < 0 or role_index >= len(roles):
                raise IndexError
            selected_role = roles[role_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please select a valid role number.")
    
    # Add the user with the selected role
    add_user(name, last, email, selected_role.id)
    session.close()
