from datetime import datetime
import uuid
from models.user import User


def find_user_by_email(users, email):
    for user in users:
        if user["email"].strip().lower() == email.strip().lower():
            return user
    return None


def validate_login(users, email, password):
    for user in users:
        if user["email"].strip().lower() == email.strip().lower() and user["password"] == password:
            return user
    return None


def register_user(users, full_name, email, password, role):
    new_user = User(
        user_id=str(uuid.uuid4()),
        full_name=full_name.strip(),
        email=email.strip().lower(),
        password=password,
        role=role,
        registered_at=str(datetime.now())
    )
    users.append(new_user.to_dict())
    return users
