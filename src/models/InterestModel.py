from src.database.db import get_connection
from src.models.entities.interest.Interest import Interest
from src.models.entities.interest.CountriesInterest import CountriesInterest
from src.models.entities.share.Ranking import Ranking

ALL_INTERESTS_QUERY = """ SELECT * FROM "T_CATALOGUE_INTEREST" """
ADD_INTEREST = """ INSERT INTO "T_USER_INTEREST" ("PROFILE_ID","INTEREST_ID") VALUES """
CLEAN_INTEREST = """ DELETE FROM "T_USER_INTEREST" WHERE "PROFILE_ID" = '{}' """
GET_INTERESTS = """ SELECT "INTEREST_ID", "CITY_CODE", "DESCRIPTION", "COUNTRY", "COUNTRY_CODE_ISO2", "COUNTRY_CODE_ISO3" FROM "T_USER_INTEREST" INNER JOIN "T_CATALOGUE_INTEREST" ON "T_USER_INTEREST"."INTEREST_ID" = "T_CATALOGUE_INTEREST"."ID" WHERE "PROFILE_ID" = '{}' """
ADD_INTEREST_CATALOGUE = """ INSERT INTO "T_CATALOGUE_INTEREST" ("CITY_CODE", "DESCRIPTION", "COUNTRY", "COUNTRY_CODE_ISO2", "COUNTRY_CODE_ISO3") VALUES """
GET_FLIGHTS_PER_DATE = """ SELECT * FROM "T_USER_INTEREST" WHERE "CREATION_DATE" > %s AND "CREATION_DATE" < %s; """
GET_UNIQUE_INTERESTS = """ SELECT DISTINCT "INTEREST_ID", "COUNTRY", "COUNTRY_CODE_ISO2", "COUNTRY_CODE_ISO3" FROM "T_USER_INTEREST" INNER JOIN "T_CATALOGUE_INTEREST" ON "T_USER_INTEREST"."INTEREST_ID" = "T_CATALOGUE_INTEREST"."ID" WHERE "PROFILE_ID" = %s; """

DELETE_USER_INTEREST_TABLE = """ DELETE FROM "T_USER_INTEREST" """
DELETE_INTERESTS_TABLE = """ DELETE FROM "T_CATALOGUE_INTEREST" """
RESET_SEQUENCE = """ ALTER SEQUENCE "T_CATALOGUE_INTEREST_ID_seq" RESTART """ 

class InterestModel():
    @classmethod
    def get_all(self):
        try:
            conn = get_connection()
            interest = []
            with conn.cursor() as cur:
                cur.execute(ALL_INTERESTS_QUERY)
                resultset = cur.fetchall()

                for row in resultset:
                    user = Interest(row[0],row[1],row[2],row[3],row[4],row[5])
                    interest.append(user.to_JSON())

            conn.close()
            return interest
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_interests(self, interests):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                argument_string = ",".join("('%s', '%s')" % (x, y) for (x, y) in interests)
                cur.execute(ADD_INTEREST + argument_string )
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def clean_interests(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CLEAN_INTEREST.format(profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def clean_interest_table(self):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_USER_INTEREST_TABLE)
                conn.commit()
                cur.execute(DELETE_INTERESTS_TABLE)
                conn.commit()
                cur.execute(RESET_SEQUENCE)
                conn.commit()
            conn.close()
            return 'success'
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_interests(self, profile_id):
        try:
            conn = get_connection()
            interest_list = []
            with conn.cursor() as cur:
                cur.execute(GET_INTERESTS.format(profile_id))
                resultset = cur.fetchall()

                for row in resultset:
                    interest = Interest(row[0],row[1],row[2],row[3],row[4],row[5])
                    interest_list.append(interest.to_JSON())
            conn.close()
            data = {"profile_id": profile_id, "interest_list": interest_list}
            return data
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_interests_catalogue(self, interests):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                argument_string = ",".join("('%s', '%s', '%s', '%s', '%s')" \
                                           % (x['city_code'], x['city'], x['country'], x['country_code_iso2'], x['country_code_iso3']) for x in interests)
                cur.execute(ADD_INTEREST_CATALOGUE + argument_string)
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_flights_per_date(self, init_date, final_date):
        try:
            conn = get_connection()
            ranking_list = []
            with conn.cursor() as cur:
                cur.execute(GET_FLIGHTS_PER_DATE, (init_date, final_date))
                resultset = cur.fetchall()
                for row in resultset:
                    result = Ranking(row[0], row[1])
                    ranking_list.append(result.to_JSON())
            conn.close()
            return ranking_list
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_unique_interests(self, profile_id):
        try:
            conn = get_connection()
            ranking_list = []
            with conn.cursor() as cur:
                cur.execute(GET_UNIQUE_INTERESTS, (profile_id, ))
                resultset = cur.fetchall()
                for row in resultset:
                    result = CountriesInterest(row[0], row[1], row[2], row[3])
                    ranking_list.append(result.to_JSON())
            conn.close()
            return ranking_list
        except Exception as ex:
            raise Exception(ex)