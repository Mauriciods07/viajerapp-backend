import datetime
import jwt
import pytz
from decouple import config

class Security():
    
    secret_key = config('JWT_KEY')
    tz = pytz.timezone("America/Mexico_City")

    @classmethod
    def generate_token(self, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=10),
            'id': authenticated_user.id,
            'email': authenticated_user.email,
            'name': authenticated_user.name,
        }

        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    @classmethod
    def verify_user_token(self, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, self.secret_key, algorithms=["HS256"])
                    user_type = payload['role_id']
                    if user_type == 1:
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False

    @classmethod
    def verify_admin_token(self, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, self.secret_key, algorithms=["HS256"])
                    role = payload['role']
                    level = payload['level']
                    if role == 1 or level == 'admin':
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False
    
    @classmethod
    def verify_influex_token(self, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, self.secret_key, algorithms=["HS256"])
                    role = payload['role']
                    level = payload['level']
                    if role == 2 or level == 'master':
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False