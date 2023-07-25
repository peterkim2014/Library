from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re #Regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "library_app"

    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.real_name = data['real_name']
        self.gender = data['gender']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        @classmethod 
        def get_all(cls):
            query = "SELECT * FROM users;"
            users = []
            results = connectToMySQL(cls.db).query_db(query)
            for row in results: 
                users.append(cls(row))
            return users
        
        @classmethod 
        def get_by_id(cls,data):
            query = """
                    SELECT * FROM users
                    LEFT JOIN saves ON users.id = saves.user_id
                    LEFT JOIN books ON books.id = saves.book_id
                    WHERE users.id = %(id)s
                    ORDER BY saves.created_at DESC;
                    """
            results = connectToMySQL(cls.db).query_db(query, data)
            user = cls(results[0])
            for row in results: 
                if row ['books.id'] == None: 
                    break
                data = {
                    "id": row['books.id'],
                    "title": row['title'],
                    'author': row['author'],
                    'pages': row['pages'],
                    'publisher': row['publisher'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                }

        #POST METHODS



        #VALIDATIONS