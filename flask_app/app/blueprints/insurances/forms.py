from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MakeInsuranceForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])

