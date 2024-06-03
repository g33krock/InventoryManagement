"""
Author: Collin Maassen, with assistance from my friends Dallas Lovell and Will Baird

Course: CSE 111

Professor Lindstrom

Date: 06/05/2024

"""

from models import User, Role

def get_roles(session):
    """Retrieve all roles from the database."""
    return session.query(Role).all()

def add_user(session):
    name = input("Enter first name: ")
    last = input("Enter last name: ")
    email = input("Enter email: ")

    # Fetch roles from the database
    roles = get_roles(session)

    # Display roles to the user
    print("Available roles:")
    for idx, role in enumerate(roles):
        print(f"{idx + 1}. {role.role}")

    # Select role
    while True:
        try:
            role_index = int(input("Select role by number: ")) - 1
            if role_index < 0 or role_index >= len(roles):
                raise IndexError
            selected_role = roles[role_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please select a valid role number.")

    try:
        # Create a new user
        new_user = User(name=name, last=last, email=email, role_id=selected_role.id)
        session.add(new_user)
        session.commit()
        print(f"User {name} {last} added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add user: {e}")
