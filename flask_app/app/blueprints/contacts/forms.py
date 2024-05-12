from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, InputRequired


class MakeContactForm(FlaskForm):
    company = SelectField('Company')
    name = StringField('Name', validators=[DataRequired()])
    phone_number = IntegerField('Phone number', validators=[InputRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Register Insurance')

    