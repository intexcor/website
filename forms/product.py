from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired


class ProductFrom(FlaskForm):
    img_prod = FileField('Аватар', validators=[FileAllowed(['jpg', 'jpeg', 'png'], DataRequired())])
    name_ooo = StringField('Название товара', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    submit = SubmitField('Создать объявление')