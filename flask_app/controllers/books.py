from flask_app import app
from flask import Flask, redirect, render_template, request, flash, session
from flask_app.models.book import Book

@app.route("/book")
def book_list():
    return render_template("book.html")

@app.route("/add_book", methods=["POST"])
def add_book_to_list():

    if Book.validate_book(request.form):
        data = {
            "title": request.form["title"],
            "author": request.form["author"],
            "pages": request.form["pages"],
            "publisher": request.form["publisher"]
        }
        Book.add_book(data)
        flash("Book successfully added")
        redirect("/book")
    else:
        flash("There was an error. Please fill in the inputs")
        redirect("/book") 