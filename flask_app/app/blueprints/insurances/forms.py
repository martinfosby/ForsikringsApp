from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired


class MakeInsuranceForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    unit_type_id = SelectField('Unit Type', coerce=int)
    customer_id = ""
    value = IntegerField('Value', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    due_date = StringField('Due Date', validators=[DataRequired()])
    company_id = SelectField('Company', coerce=int)
    submit = SubmitField('Register Insurance')