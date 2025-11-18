from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from app.models import Ad


class AdForm(FlaskForm):
    """Ad creation/edit form"""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=3, max=200, message='Title must be between 3 and 200 characters')
    ])
    description = TextAreaField('Description (Markdown supported)', validators=[
        DataRequired(),
        Length(min=10, max=5000, message='Description must be between 10 and 5000 characters')
    ])
    category = SelectField('Category', validators=[DataRequired()], choices=Ad.CATEGORIES)
