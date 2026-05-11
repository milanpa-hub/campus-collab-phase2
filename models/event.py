class Event:
    def __init__(self, session_id, host_id, title, category, date, time, location, description, status, created_at):
        self.session_id = session_id
        self.host_id = host_id
        self.title = title
        self.category = category
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self.status = status
        self.created_at = created_at

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "host_id": self.host_id,
            "title": self.title,
            "category": self.category,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
        }
