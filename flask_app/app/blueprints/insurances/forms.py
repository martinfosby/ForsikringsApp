from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class MakeInsuranceForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    unit_type_id = SelectField('Unit Type', coerce=int)
    customer_id = "test"
    value = IntegerField('Value', validators=[InputRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    due_date = StringField('Due Date', validators=[DataRequired()])
    company_id = SelectField('Company', coerce=int)
    submit = SubmitField('Register Insurance')

class DropDownForm(FlaskForm):
    insuranceStatus = SelectField(
        'Insurance Status', 
        validators=[DataRequired()], 
        choices=[('insured', 'Insured'), ('uninsured', 'Un-insured'), ('insured_uninsured', 'Insured/Uninsured')]
    )
    submit = SubmitField('Filter')
    