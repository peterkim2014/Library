from flask import Flask, render_template, session, redirect, request, flash
from flask_app.models.user import User
from flask_app.models.book import Book 
from flask_app import app

@app.route('/books/add_book')
def new_book():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id': session['user_id']
        }
    return render_template('book.html', user=User.get_by_id(data))

#POST METHODS

@app.route('/books/add', methods=['POST'])
def add_book():
    if 'user_id' not in session:
        return redirect('/')
    if not Book.validate_book(request.form):
        return redirect('/books/add_book')
    data = {
        'id': id,
        "title": request.form['title'],
        "author": request.form['author'],
        "pages": request.form['pages'],
        "publisher": request.form['publisher']
    }
    Book.add_book(data)
    return redirect('/home')