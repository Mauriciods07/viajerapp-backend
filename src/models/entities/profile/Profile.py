class Profile():
    def __init__(self, email, name, profile_photo) -> None:
        self.email = email
        self.name = name
        self.profile_photo = profile_photo

    def to_JSON(self):
        return {
            'name': self.name,
            'email': self.email,
            'profile_photo': self.profile_photo
        }