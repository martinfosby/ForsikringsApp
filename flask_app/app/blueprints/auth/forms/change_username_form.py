from . import *

class ChangeUsernameForm(FlaskForm):
    new_username = StringField('New username', validators=[DataRequired()])
    submit = SubmitField('Change username')