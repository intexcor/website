from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_lead = StringField('Тим-лид', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    worksize = IntegerField('Время работы', validators=[DataRequired()])
    collaborators = StringField('ID работников', validators=[DataRequired()])
    start_date = DateField('Начало')
    end_date = DateField('Конец')
    is_finished = BooleanField('Завершено/не завершено')
    submit = SubmitField('Применить')