from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('Username or Hashtag', validators=[DataRequired()])
    submitUsername = SubmitField('Username')
    submitHashtag = SubmitField('Hashtag')
