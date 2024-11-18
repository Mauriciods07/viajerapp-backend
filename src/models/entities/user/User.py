class User():
    def __init__(self, name, email, profile_photo) -> None:
        self.name = name
        self.email = email
        self.profile_photo = profile_photo

    def to_JSON(self):
        return {
            'name': self.name,
            'email': self.email,
            'profile_photo': self.profile_photo
        }