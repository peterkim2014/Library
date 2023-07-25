from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import MySQLConnection

@app.route("/")
def welcome_page():
    return render_template("welcome_page.html")
