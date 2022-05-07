from flask_app.config.mysqlconnection import MySQLConnection
from datetime import datetime
import math

class Message:
    db_name = "recoma_base"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.sender_id = data["sender_id"]
        self.sender = data["sender"]
        self.receiver_id = data["receiver_id"]
        self.receiver = data["receiver"]

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def save_message(cls, data):
        query = "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s);"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        return results  

    @classmethod
    def get_messages(cls, data):
        query = "SELECT residents.first_name as sender, residents2.first_name as receiver, messages.* FROM residents LEFT JOIN messages ON residents.id = messages.sender_id LEFT JOIN residents as residents2 ON residents2.id = messages.receiver_id WHERE residents2.id = %(id)s;"
        results = MySQLConnection(cls.db_name).query_db(query, data)
        messages = []   
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return MySQLConnection(cls.db_name).query_db(query, data)
