from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import book
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
        self.saved_books = []

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM users;"
        users = []
        results = connectToMySQL(cls.db).query_db(query)
        for row in results: 
            users.append(cls(row))
        return users
    
    @classmethod
    def get_by_username(cls, data):
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
        
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
            user.saved_books.append(book.Book(data))
        print(user)
        return user

#POST METHODS
    #REGISTER USER
    @classmethod
    def register_user(cls,data):
        query = """
                INSERT INTO users(username, email, password)
                VALUES (%(username)s, %(email)s, %(password)s);
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    
    @classmethod
    def update_user(cls, form_data):
        query = """
                UPDATE users
                SET real_name = %(real_name)s,
                gender = %(gender)s,
                updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, form_data)



    #LOGIN 
    @classmethod
    def find_user(cls, data):
        query = """
        SELECT * FROM users WHERE username = %(username)s;
        """
        result = MySQLConnection(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        else:
            return cls(result[0])
        

    #SAVE BOOK
    @classmethod
    def add_book(cls,data):
        query = """
                INSERT INTO saves (user_id, book_id)
                VALUES (%(user_id)s, %(book_id)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)

    #UNSAVE BOOK 
    @classmethod
    def remove_book(cls, form_data):
        query=  """
                DELETE FROM saves 
                WHERE user_id = %(user_id)s
                AND book_id = %(book_id)s;
                """
        print(query)
        return connectToMySQL(cls.db).query_db(query,form_data)

    #VALIDATIONS
    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s OR username = %(username)s;
                """
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['username']) < 3: 
            flash("User name must be longer than 3 characters", 'reg_error')
            is_valid = False

        if len(results) >= 1:
            flash("Email address or username is already registered", 'reg_error')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'reg_error')
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must contain more than 8 characters", 'reg_error')
            is_valid = False
            
        if user['password'] != user['confirm-password']:
            flash("Passwords don't match", 'reg_error')
            is_valid = False

        print(user['password'])
        print(is_valid)

        return is_valid 