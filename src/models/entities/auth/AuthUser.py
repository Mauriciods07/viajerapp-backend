class AuthUser():

    def __init__(self, profile_id, email, name, password):
        self.id = profile_id
        self.email = email
        self.name = name
        self.password = password

    def to_JSON(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'password': self.password
        }