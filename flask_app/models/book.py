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
        
        #POST METHODS
    @classmethod #Save/Add a new book 
    def add_book(cls, form_data):
        query = """
                INSERT INTO books (title, author, pages, publisher)
                VALUES (%(title)s, %(author)s, %(pages)s, %(publisher)s);
                """
        print(query)
        results = connectToMySQL(cls.db).query_db(query, form_data)
        print(results) 
        return results
        
    @classmethod #Edit 
    def update_book(cls,form_data):
        query = """
                UPDATE books
                SET title = %(title)s,
                author = %(author)s,
                pages = %(pages)s, 
                publisher = %(publisher)s,
                updated_at = NOW()
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query,form_data)
        return results
        
    @classmethod
    def eliminate(cls,data):
        query = """
                DELETE FROM books
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results



        #VALIDATIONS
    @staticmethod
    def validate_book(book):
        is_valid = True
        query = """
                SELECT * FROM books
                WHERE title = %(title)s
                AND author = %(author)s;
                """
        #Since there are books that share the same title, the query makes sure to check if both the title and author are the same before rejecting it
        results = connectToMySQL(Book.db).query_db(query, book)

        if len(results) >= 1: 
            flash("Book is already part of our database")
            is_valid = False

        if len(book['title']) < 1:
            flash("Must include a title for this book")
            is_valid = False
            
        if len(book['author']) < 3: 
            flash("Must include the author of the book")
            is_valid = False
            
        print(is_valid)
        return is_valid


