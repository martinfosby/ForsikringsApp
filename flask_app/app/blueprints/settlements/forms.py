from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class MakeSettlementForm(FlaskForm):
    insurance_label = SelectField('Insurance Label', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    sum = IntegerField('Sum', validators=[DataRequired()])
    submit = SubmitField('Register Settlement')


class DeleteSettlementForm(FlaskForm):
    submit = SubmitField('Delete Settlement')


class DropDownPaidForm(FlaskForm):
    settlementStatus = SelectField(
        'Settlement Status', 
        validators=[DataRequired()], 
        choices=[('all', 'All'), ('paid', 'Paid'), ('unpaid', 'Unpaid')]
    )
    submit = SubmitField('Filter')

class DropDownInsuranceForm(FlaskForm):
    settlementStatus = SelectField(
        'Settlement Status', 
        validators=[DataRequired()], 
        choices=[('all', 'All')]
    )
    submit = SubmitField('Filter')