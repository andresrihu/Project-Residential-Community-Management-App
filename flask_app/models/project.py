from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from flask_app import app
from flask_app.models import resident


class Project:
    db_name = "recoma_base"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.resident_id = data["resident_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.votes = data["votes"]
        self.resident = []

    @staticmethod
    def validate_project(form_data):
        is_valid = True
        if len(form_data["name"]) < 2:
            flash("Project Name must have at least 5 characters.")
            is_valid = False
        
        if len(form_data["description"]) < 10:
            flash("Project Description must have at least 10 characters.")
            is_valid = False

        return is_valid

    # Methods
    # Create Project
    @classmethod
    def save(cls, data):
        query = "INSERT INTO projects (name, description, resident_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(resident_id)s, NOW(), NOW());"
        result = MySQLConnection(cls.db_name).query_db(query, data)
        return result

    # View One Project
    @classmethod
    def view_one(cls, data):
        query = "SELECT * FROM projects WHERE id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return cls(results[0])

    # View All Projects
    @classmethod
    def view_all(cls):
        query = "SELECT * FROM projects;"
        return MySQLConnection(cls.db_name).query_db(query)

    # Edit Project
    @classmethod
    def edit_project(cls, data):
        query = "UPDATE projects SET name = %(name)s, description = %(description)s WHERE id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return results

    # Delete Project
    @classmethod
    def delete_project(cls, data):
        query = "DELETE FROM projects WHERE id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return results

    # View all Projects joining the Resident info
    @classmethod
    def get_projects_with_resident(cls):
        query = "SELECT * FROM projects LEFT JOIN residents ON residents.id = projects.resident_id ORDER BY votes DESC;"
        results = MySQLConnection(cls.db_name).query_db(query)
        projects = []
        for row in results:
            project = cls(row)
            resident_data = {
                "id" : row["residents.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "house_id" : row["house_id"],
                "project_id" : row["project_id"],
                "message_id" : row["message_id"],
                "resident_since" : row["resident_since"],
                "phone_number" : row["phone_number"],
                "role" : row["role"],
                "about" : row["about"],
                "created_at" : row["residents.created_at"],
                "updated_at" : row["residents.updated_at"],
            }
            project.resident = resident.Resident( resident_data  )

            projects.append(project)
        return projects

    # View One Project with Resident info
    @classmethod
    def view_one_with_resident(cls, data):
        query = "SELECT * FROM projects LEFT JOIN residents on projects.resident_id = resident_id WHERE projects.id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        print(results)
        project = cls(results[0])
        resident_data = {
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
        project.resident = resident.Resident(resident_data)
        return project

    # Updating vote counter
    @classmethod
    def update_votes(cls, data):
        query = "UPDATE projects SET votes = IFNULL(votes, 0) + %(votes)s WHERE id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return results

    