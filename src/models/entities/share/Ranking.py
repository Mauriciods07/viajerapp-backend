class Ranking:
    def __init__(self, profile_id, interest_id) -> None:
        self.profile_id = profile_id
        self.interest_id = interest_id

    def to_JSON(self):
        return {
            'profile_id': self.profile_id,
            'interest_id': self.interest_id
        }
