class Claim:
    def __init__(self, claim_id, need_id, session_id, contributor_id, claimed_item, status, claimed_at):
        self.claim_id = claim_id
        self.need_id = need_id
        self.session_id = session_id
        self.contributor_id = contributor_id
        self.claimed_item = claimed_item
        self.status = status
        self.claimed_at = claimed_at

    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "need_id": self.need_id,
            "session_id": self.session_id,
            "contributor_id": self.contributor_id,
            "claimed_item": self.claimed_item,
            "status": self.status,
            "claimed_at": self.claimed_at,
        }
