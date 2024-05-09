from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, InputRequired


class MakeOfferForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    company_id = SelectField('Company', coerce=int)
    insurance_id = SelectField('Insurance', coerce=int)
    submit = SubmitField('Register Offer')
