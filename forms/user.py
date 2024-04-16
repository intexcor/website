from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    image_prof = FileField('Аватар', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    lastname = StringField('Отчество', validators=[DataRequired()])
    phone_number = StringField('Номер телефона')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
