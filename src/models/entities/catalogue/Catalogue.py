class Catalogue():

    def __init__(self, id, description) -> None:
        self.id = id
        self.description = description

    def to_JSON(self):
        return {
            'id': self.id,
            'description': self.description
        }