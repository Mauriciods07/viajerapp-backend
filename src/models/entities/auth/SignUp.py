from typing import Dict

class SignUp():
    def __init__(
            self,
            profile_id,
            email,
            password,
            name
        ) -> None:
        self.id = profile_id
        self.email = email
        self.password = password
        self.name = name

    def to_JSON(self) -> Dict[str, str]:
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name
        }