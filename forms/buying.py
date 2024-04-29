from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class BuyingForm(FlaskForm):
    submit = SubmitField('Оплатить✅')