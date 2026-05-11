class Need:
    def __init__(self, need_id, session_id, item_name, quantity_needed, quantity_claimed, notes):
        self.need_id = need_id
        self.session_id = session_id
        self.item_name = item_name
        self.quantity_needed = quantity_needed
        self.quantity_claimed = quantity_claimed
        self.notes = notes

    def remaining_quantity(self):
        return int(self.quantity_needed) - int(self.quantity_claimed)

    def to_dict(self):
        return {
            "need_id": self.need_id,
            "session_id": self.session_id,
            "item_name": self.item_name,
            "quantity_needed": self.quantity_needed,
            "quantity_claimed": self.quantity_claimed,
            "notes": self.notes,
        }
