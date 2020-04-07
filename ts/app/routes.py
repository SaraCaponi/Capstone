from flask import render_template
from app import application

@application.route('/')
@application.route('/index')
def home():
    return render_template('index.html')

@application.route('/username/')
def username():
    return render_template('username.html')

@application.route('/hashtag/')
def hashtag():
    return render_template('hashtag.html')

@application.route('/about/')
def about():
    return render_template('about.html')