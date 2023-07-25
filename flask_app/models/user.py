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
    #REGISTER USER
    @classmethod
    def register_user(cls,data):
        query = """
                INSERT INTO users(username, email, password)
                VALUES (%(username)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)


    #VALIDATIONS
    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s OR username = %(user_name)s;
                """
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['user_name']) < 3: 
            flash("User name must be longer than 3 characters", 'reg_error')
            is_valid = False

        if len(results) >= 1:
            flash("Email address or username is already registered", 'reg_error')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'reg_error')

        if len(user['password']) < 8:
            flash("Password must contain more than 8 characters", 'reg_error')
            is_valid = False
            
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", 'reg_error')

        print(user['password'])
        print(is_valid)

        return is_valid 