from src.database.db import get_connection
from src.models.entities.multimedia.MultimediaOut import MultimediaOut
from src.models.entities.multimedia.Multimedia import Multimedia

GET_MULTIMEDIA = """ SELECT "PROFILE_ID", "ARCHIVE_URL", "ARCHIVE_TYPE" FROM "T_MULTIMEDIA" WHERE "SHARE_ID" = %s AND "SHARE_TYPE" = %s """
GET_ALL_MULTIMEDIA = """ SELECT "PROFILE_ID", "SHARE_ID", "SHARE_TYPE", "ARCHIVE_URL", "ARCHIVE_TYPE" FROM "T_MULTIMEDIA" """
DELETE_MULTIMEDIA = """ DELETE FROM "T_MULTIMEDIA" WHERE "SHARE_ID" = %s AND "SHARE_TYPE" = %s """

CREATE_MULTIMEDIA = """ INSERT INTO "T_MULTIMEDIA" ("PROFILE_ID","SHARE_ID","SHARE_TYPE","ARCHIVE_URL","ARCHIVE_TYPE") VALUES (%s,%s,%s,%s,%s) """

GET_ALL_MULTIMEDIA_FILTER = """ SELECT "PROFILE_ID", "SHARE_ID", "SHARE_TYPE", "ARCHIVE_URL", "ARCHIVE_TYPE" FROM "T_MULTIMEDIA" WHERE "SHARE_ID" IN %s AND "SHARE_TYPE" = 'POST' """


class MultimediaModel():

    @classmethod
    def get_multimedia(self, share_id, share_type):
        try:
            conn = get_connection()
            multimedia_list = []
            with conn.cursor() as cur:
                cur.execute(GET_MULTIMEDIA, (share_id,share_type))
                resultset = cur.fetchall()
                for row in resultset:
                    multimedia = MultimediaOut(row[1],row[2])
                    multimedia_list.append(multimedia.to_JSON())
            return multimedia_list
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_all_multimedia(self):
        try:
            conn = get_connection()
            multimedia_list = []
            with conn.cursor() as cur:
                cur.execute(GET_ALL_MULTIMEDIA)
                resultset = cur.fetchall()
                for row in resultset:
                    multimedia = Multimedia(row[0],row[1],row[2],row[3],row[4])
                    multimedia_list.append(multimedia.to_JSON())
            return multimedia_list
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_all_multimedia_filter(self, posts):
        try:
            conn = get_connection()
            multimedia_list = []
            with conn.cursor() as cur:
                cur.execute(GET_ALL_MULTIMEDIA_FILTER, (tuple(posts),))
                resultset = cur.fetchall()
                for row in resultset:
                    multimedia = Multimedia(row[0],row[1],row[2],row[3],row[4])
                    multimedia_list.append(multimedia.to_JSON())
            return multimedia_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def create_multimedia(self, multimedia):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CREATE_MULTIMEDIA, (multimedia.profile_id ,multimedia.share_id, multimedia.share_type, multimedia.archive_url, multimedia.archive_type))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_multimedia(self, share_id, share_type):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_MULTIMEDIA,(share_id,share_type))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)