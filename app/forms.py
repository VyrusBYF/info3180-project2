from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField
from wtforms.validators import DataRequired, Email

class UploadForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    file = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])