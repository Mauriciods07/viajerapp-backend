from src.database.db import get_connection
from .entities.profile.Profile import Profile

GET_PROFILE_DATA = """ SELECT "EMAIL","NAME","PROFILE_PHOTO" FROM "T_PROFILE" WHERE "ID" = %s """

class ProfileModel():

    @classmethod
    def get_profile_data(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(GET_PROFILE_DATA, (profile_id,))
                row = cur.fetchone()
                user = Profile(row[0],row[1],row[2])
            conn.close()
            return user.to_JSON()
        except Exception as ex:
            raise Exception(ex)