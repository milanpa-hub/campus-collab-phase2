class User:
    def __init__(self, user_id, full_name, email, password, role, registered_at):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.role = role
        self.registered_at = registered_at

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "registered_at": self.registered_at,
        }
