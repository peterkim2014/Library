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

@app.route('/books/<int:id>')
def view_book(id):
    if 'user_id' not in session: 
        return redirect('/')
    else: 
        data = {
            'id': session['user_id']
        }
    return render_template('book_view.html', user=User.get_by_id(data), book=Book.get_by_id({'id':id}))

@app.route('/edit_book/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/')
    else: 
        data = {
            'id': session['user_id']
        }
    return render_template('book_edit.html', user=User.get_by_id(data), book=Book.get_by_id({'id':id}))


#POST METHODS

@app.route('/books/add', methods=['POST'])
def add_book():
    if 'user_id' not in session:
        return redirect('/')
    if not Book.validate_book(request.form):
        return redirect('/books/add_book')
    form_data = {
        "title": request.form['title'],
        "author": request.form['author'],
        "pages": request.form['pages'],
        "publisher": request.form['publisher']
    }
    print(form_data)
    Book.add_book(form_data)
    return redirect('/home')

@app.route('/books/edit_process/<int:id>', methods=['POST'])
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
        "title": request.form['title'],
        "author": request.form['author'],
        "pages": request.form['pages'],
        "publisher": request.form['publisher']
    }
    print(data)
    Book.update_book(data)
    return redirect(f"/books/{id}")