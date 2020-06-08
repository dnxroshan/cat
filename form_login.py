
from flask_wtf import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators

class FormLogin(Form):
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

