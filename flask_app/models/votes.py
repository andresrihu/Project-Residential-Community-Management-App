from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

class Vote:
    db_name = "recoma_base"
    def __init__(self, data):
        self.vote_for_id = data["vote_for_id"]
        self.unique_vote_id = data["unique_vote_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # Validate the Vote
    @staticmethod
    def validate_vote(form_data):
        is_valid = True
        query = "SELECT * FROM votes WHERE vote_for_id = %(id)s AND unique_vote_id = %(resident_id)s;"
        results = MySQLConnection("recoma_base").query_db(query, form_data)
        print("*************validation****************")
        print(results)
        if len(results) > 0:
            flash("You can only vote once per project.")
            is_valid = False

        return is_valid

    # Create a vote
    @classmethod
    def save(cls, data):
        query = "INSERT INTO votes (vote_for_id, unique_vote_id, created_at, updated_at) VALUES (%(id)s, %(resident_id)s, NOW(), NOW());"
        return MySQLConnection(cls.db_name).query_db(query, data)

