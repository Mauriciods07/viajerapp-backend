from src.database.db import get_connection
from .entities.user.User import User

UPDATE = """ UPDATE "T_PROFILE" SET "NAME" = %s WHERE  "ID" = %s; """
UPDATE_PHOTO = """ UPDATE "T_PROFILE" SET "PROFILE_PHOTO" = %s, "NAME" = %s WHERE  "ID" = %s; """
GET_USER_DATA = """ SELECT "NAME", "EMAIL", "PROFILE_PHOTO" FROM "T_PROFILE" WHERE "ID" = %s """
UPDATE_PASSWORD = """ UPDATE "T_PROFILE" SET "PASSWORD" = %s WHERE "ID" = %s """

class UsersModel():
    @classmethod
    def update_user(self, profile_id, name):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE, (name,profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_data_photo_user(self, profile_id, profile_photo, name):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_PHOTO, (profile_photo,name,profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_data(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(GET_USER_DATA, (profile_id,))
                row = cur.fetchone()
                user = User(row[0],row[1],row[2])
            conn.close()
            return user.to_JSON()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_password(self, password, profileId):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_PASSWORD, (password,profileId))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)