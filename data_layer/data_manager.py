import json
from pathlib import Path
from datetime import datetime, date


class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.users_path = self.data_dir / "users.json"
        self.sessions_path = self.data_dir / "sessions.json"
        self.needs_path = self.data_dir / "needs.json"
        self.claims_path = self.data_dir / "claims.json"

    def load_json(self, path: Path):
        if not path.exists():
            return []
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def save_json(self, path: Path, data):
        path.write_text(json.dumps(data, indent=4), encoding="utf-8")

    def load_users(self):
        return self.load_json(self.users_path)

    def save_users(self, users):
        self.save_json(self.users_path, users)

    def load_sessions(self):
        return self.load_json(self.sessions_path)

    def save_sessions(self, sessions):
        self.save_json(self.sessions_path, sessions)

    def load_needs(self):
        return self.load_json(self.needs_path)

    def save_needs(self, needs):
        self.save_json(self.needs_path, needs)

    def load_claims(self):
        return self.load_json(self.claims_path)

    def save_claims(self, claims):
        self.save_json(self.claims_path, claims)

    def ensure_sample_data(self):
        if not self.users_path.exists():
            self.save_users([
                {
                    "user_id": "host-demo-1",
                    "full_name": "Demo Host",
                    "email": "host@udel.edu",
                    "password": "host123",
                    "role": "Host",
                    "registered_at": str(datetime.now())
                },
                {
                    "user_id": "contrib-demo-1",
                    "full_name": "Demo Contributor",
                    "email": "student@udel.edu",
                    "password": "student123",
                    "role": "Contributor",
                    "registered_at": str(datetime.now())
                }
            ])

        if not self.sessions_path.exists():
            self.save_sessions([
                {
                    "session_id": "session-1",
                    "host_id": "host-demo-1",
                    "title": "MISY350 Debugging Night",
                    "category": "Study Session",
                    "date": str(date.today()),
                    "time": "6:00 PM",
                    "location": "Morris Library Room 114",
                    "description": "Bring your Streamlit bugs and we will work through them together.",
                    "status": "Open",
                    "created_at": str(datetime.now())
                }
            ])

        if not self.needs_path.exists():
            self.save_needs([
                {
                    "need_id": "need-1",
                    "session_id": "session-1",
                    "item_name": "Extension Cord",
                    "quantity_needed": 2,
                    "quantity_claimed": 0,
                    "notes": "Any length is fine"
                },
                {
                    "need_id": "need-2",
                    "session_id": "session-1",
                    "item_name": "Practice Questions",
                    "quantity_needed": 5,
                    "quantity_claimed": 0,
                    "notes": "Printed or digital"
                }
            ])

        if not self.claims_path.exists():
            self.save_claims([])
