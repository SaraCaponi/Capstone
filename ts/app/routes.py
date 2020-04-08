from flask import render_template
from app import application
from app.forms import SearchForm

@application.route('/')
@application.route('/index/')
def home():
    form = SearchForm()
    return render_template('index.html', form=form)

@application.route('/username/')
def username():
    return render_template('username.html')

@application.route('/hashtag/')
def hashtag():
    return render_template('hashtag.html')

@application.route('/about/')
def about():
    return render_template('about.html')