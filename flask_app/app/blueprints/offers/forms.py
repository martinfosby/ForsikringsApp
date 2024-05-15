from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, InputRequired


class MakeOfferForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    company_id = SelectField('Company')
    insurance_id = SelectField('Insurance')
    submit = SubmitField('Register Offer')


class DeleteOfferForm(FlaskForm):
    submit = SubmitField('Delete Offer')


class DropDownForm(FlaskForm):
    offerStatus = SelectField(
        'Offer Status', 
        validators=[DataRequired()], 
        choices=[('all', 'All')]
    )
    submit = SubmitField('Filter')