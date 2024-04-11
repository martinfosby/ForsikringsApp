from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class MakeSettlementForm(FlaskForm):
    insurance_id = IntegerField('Insurance ID', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    sum = IntegerField('Sum', validators=[DataRequired()])
    submit = SubmitField('Register Settlement')