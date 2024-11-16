class Interest():
    
    def __init__(self, interest_id, description) -> None:
        self.interest_id = interest_id
        self.description = description

    def to_JSON(self):
        return {
            'interest_id': self.interest_id,
            'description': self.description
        }