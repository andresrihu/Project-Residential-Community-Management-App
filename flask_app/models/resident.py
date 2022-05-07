from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from flask_app import app
from flask_app.models import house
from datetime import datetime
import math

now = datetime.now()

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^([\(]{1}[0-9]{3}[\)]{1}[\.| |\-]{0,1}|^[0-9]{3}[\.|\-| ]?)?[0-9]{3}(\.|\-| )?[0-9]{4}$')


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Resident:
    db_name = "recoma_base"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.house_id = data["house_id"]
        self.project_id = data["project_id"]
        self.message_id = data["message_id"]
        self.resident_since = data["resident_since"]
        self.phone_number = data["phone_number"]
        self.role = data["role"]
        self.about = data["about"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # def time_span(self):
    #     now = datetime.now()
    #     delta = now - self.resident_since
    #     print(delta.years)
    #     print(delta.total_months())
    #     if delta.years > 0:
    #         return f"Resident for {delta.years} years in Las Veredas"


    # Validations - validate registration
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 2:
            flash("First name must have at least 2 characters.")
            is_valid = False
        
        if len(form_data["last_name"]) < 2:
            flash("Last name must have at least 2 characters.")
            is_valid = False

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = MySQLConnection("recoma_base").query_db(query, form_data)
        if  results > 1:
            flash("Email in our records, please login.")
            is_valid = False
        
        if not EMAIL_REGEX.match(form_data["email"]):
            flash("Invalid email address!")
            is_valid = False

        if form_data["house_id"] == "Select Your Residence":
            flash("Please select your residence number.")
            is_valid = False

        if len(form_data["password"]) < 8:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        
        if form_data["password"] != form_data["confirm_password"]:
            flash("Passwords must match.")
            is_valid = False

        return is_valid

    # Validations - validate login
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        user_from_db = Resident.get_user_by_email(form_data)

        if not user_from_db:
            flash("Invalid Email: Email not found")
            is_valid = False

        elif not bcrypt.check_password_hash(user_from_db.password, form_data["password"]):
            flash("Invalid Password")
            is_valid = False

        return is_valid

    # Validate Edit Resident
    @staticmethod
    def validate_edit_resident(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 2:
            flash("First name must have at least 2 characters.")
            is_valid = False
        
        if len(form_data["last_name"]) < 2:
            flash("Last name must have at least 2 characters.")
            is_valid = False

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = MySQLConnection("belt_exam").query_db(query, form_data)
        if len(results) > 1:
            flash("Email in our records, please try a different email.")
            is_valid = False
        
        if not EMAIL_REGEX.match(form_data["email"]):
            flash("Invalid email address!")
            is_valid = False

        if str(form_data["phone_number"]) > str(0) and not PHONE_REGEX.match(form_data["phone_number"]):
            flash("Invalid Phone Number. Use 3 digit area code, followed by 7 digits. 10 digits total")
            is_valid = False

        return is_valid

    # Methods
    # Create a user
    @classmethod
    def save(cls, data):
        query = "INSERT INTO residents (first_name, last_name, email, password, house_id, about, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(house_id)s, %(about)s, NOW(), NOW());"
        result = MySQLConnection(cls.db_name).query_db(query, data)
        return result

    # Find user by email
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM residents WHERE email = %(email)s;"
        result = MySQLConnection(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    # View One Resident
    @classmethod
    def view_one_resident(cls, data):
        query = "SELECT * FROM residents WHERE id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return cls(results[0])

    # View All Residents
    @classmethod
    def view_all_residents(cls):
        query = "SELECT * FROM residents;"
        return MySQLConnection(cls.db_name).query_db(query)

    # Edit Resident Info
    @classmethod
    def edit_resident(cls, data):
        query = "UPDATE residents SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, resident_since = %(resident_since)s, phone_number = %(phone_number)s, role = %(role)s, about = %(about)s WHERE id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return results

    # View One Resident with House information attached
    @classmethod
    def view_one_with_house(cls, data):
        query = "SELECT * FROM residents LEFT JOIN houses on residents.house_id = houses.id WHERE residents.id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        print(results)
        resident = cls(results[0])
        house_data = {
                "id" : results[0]["houses.id"],
                "number" : results[0]["number"],
                "created_at" : results[0]["houses.created_at"],
                "updated_at" : results[0]["houses.updated_at"],
            }
        resident.house = house.House(house_data)
        return resident

    # Attach Resident to Project Vote using project_id
    @classmethod
    def project_vote(cls, data):
        query = "UPDATE residents SET project_id = %(id)s WHERE id = %(resident_id)s;"
        return MySQLConnection(cls.db_name).query_db(query, data)

