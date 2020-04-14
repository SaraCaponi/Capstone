from flask import render_template, flash, redirect
from app import application
from app.forms import SearchForm

@application.route('/', methods=['GET', 'POST'])
@application.route('/index/', methods=['GET', 'POST'])
def home():
    form = SearchForm()

    if form.validate_on_submit():
        flash('Query {}'.format(form.query.data))
        return render_template('index.html', form=form, data=form.query.data)


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