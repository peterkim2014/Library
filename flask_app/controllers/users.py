from flask_app import app
from flask import Flask, redirect, render_template, request, flash, session
from ..models.user import User
# from ..models.book import Book
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
dataFormat = "%#m/%#d/%Y %I: %M %p"

@app.route('/')
def login_and_reg():
    return render_template("welcome_page.html")

@app.route('/home')
def home_page():
    if 'user_id' not in session: 
        return redirect ('/')
    else: 
        data = {
            'id': session['user_id']
        }
    return render_template('home.html', user=User.get_by_id(data))

@app.route('/users')
def all_users():
    if 'user_id' not in session: 
        return redirect ('/')
    else: 
        data ={
            'id': session['user_id']
        }
    return render_template('users.html', users=User.get_all(), user=User.get_by_id(data))

@app.route('/users/<int:id>')
def user_profile(id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        session_data = {
            'id': session['user_id']
        }
        data = {
            "id": id
        }
        return render_template('profile.html', session_user=User.get_by_id(session_data), user=User.get_by_id(data))

#ACTIONS/POSTS 
@app.route('/register', methods=['POST'])
def reg():
    if not User.validate_reg(request.form):
        return redirect('/')
    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.register_user(data)
    session['user_id'] = id

    return redirect('/home')

@app.route('/login', methods=['POST'])
def login():
    data = { 'username': request.form['username'] }
    user_in_db = User.find_user(data)
    if not user_in_db:
        flash('Invalid UserName/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid UserName/Password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    print(user_in_db)
    print(session['user_id'])
    session['logged_in'] = True
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')