# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from wtforms import ValidationError


import os

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Movie Poster', validators=[DataRequired()])

    def is_valid(form, field):
        file = field.data
        filename = secure_filename(file.filename)
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            raise ValidationError('Invalid file type. Allowed types are: png, jpg, jpeg, gif')