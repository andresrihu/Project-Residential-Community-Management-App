from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from flask_app import app
from flask_app.models import resident


class House:
    db_name = "recoma_base"
    def __init__(self, data):
        self.id = data["id"]
        self.number = data["number"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.residents =[]

    @classmethod
    def show_all(cls):
        query = "SELECT * FROM houses"
        return MySQLConnection(cls.db_name).query_db(query)

    # find house residents:
    # @classmethod
    # def get_house_residents(cls,data):
    #     print("*******************************")
    #     query = "SELECT * FROM houses LEFT JOIN residents ON houses.id = residents.house_id WHERE house_id = %(id)s;"
    #     results = MySQLConnection(cls.db_name).query_db(query, data)
    #     print(results)
    #     if len(results) < 1:
    #         # flash there are no residents registered for this house
    #         return False
    #     house = cls(results[0])
    #     for row in results:
    #         resident_data = {
    #             "id" : row["residents.id"],
    #             "first_name" : row["first_name"],
    #             "last_name" : row["last_name"],
    #             "email" : row["email"],
    #             "password" : row["password"],
    #             "house_id" : row["house_id"],
    #             "project_id" : row["project_id"],
    #             "message_id" : row["message_id"],
    #             "resident_since" : row["resident_since"],
    #             "phone_number" : row["phone_number"],
    #             "role" : row["role"],
    #             "about" : row["about"],
    #             "created_at" : row["residents.created_at"],
    #             "updated_at" : row["residents.updated_at"],
    #         }
    #         house.residents.append(resident.Resident(resident_data))
    #     return house

    # View One House with Resident information attached
    @classmethod
    def view_one_with_resident(cls, data):
        query = "SELECT * FROM houses LEFT JOIN residents on residents.house_id = houses.id WHERE houses.id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        print(results)
        house = cls(results[0])
        resident_data = resident_data = {
                "id" : results[0]["residents.id"],
                "first_name" : results[0]["first_name"],
                "last_name" : results[0]["last_name"],
                "email" : results[0]["email"],
                "password" : results[0]["password"],
                "house_id" : results[0]["house_id"],
                "project_id" : results[0]["project_id"],
                "message_id" : results[0]["message_id"],
                "resident_since" : results[0]["resident_since"],
                "phone_number" : results[0]["phone_number"],
                "role" : results[0]["role"],
                "about" : results[0]["about"],
                "created_at" : results[0]["residents.created_at"],
                "updated_at" : results[0]["residents.updated_at"],
            }
        house.resident = resident.Resident(resident_data)
        return house