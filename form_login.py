
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators

class FormLogin(FlaskForm):
    username = TextField(
        'username',
        validators=[
            validators.DataRequired(),
        ]
    )
    
    password = PasswordField(
        'password',
        validators=[
            validators.DataRequired()
        ]
    )

    submit = SubmitField(
        'submit',
        validators=[
            validators.DataRequired()
        ]
    )

