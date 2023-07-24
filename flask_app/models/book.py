from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app.models import user
from flask import flash

class Book: 
    db = "library_app"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.author = db_data['author']
        self.pages = db_data['pages']
        self.publisher = db_data['publisher']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.saved_by = []

        @classmethod
        def get_all(cls):
            query = """
                    SELECT * FROM books
                    """
            results = connectToMySQL(cls.db).query_db(query)

            return results
        
        @classmethod 
        def get_by_id(cls,data):
            query = """
                    SELECT * FROM books
                    LEFT JOIN saves ON books.id = book_id 
                    LEFT JOIN users ON user_id = users.id
                    WHERE books.id = %(id)s;
                    """
            results = connectToMySQL(cls.db).query_db(query,data)
            book = cls(results[0])
            for row in results:
                if row['users.id'] == None:
                    break
                data = {
                    "id": row['users.id'],
                    'username': row['username'],
                    'email': row['email'],
                    'password': "",
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                book.saved_by.append(user.User(data))
            return book 
        
        @classmethod 
        def add_movie(cls, form_data):
            query = """
                    INSERT INTO books (title, author, pages, publisher)
                    VALUES (%(title)s, %(author)s, %(page)s, %(publisher)s);
                    """
            results = connectToMySQL(cls.db).query_db(query, form_data)
            print(results) 
            return results