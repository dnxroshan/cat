
from flask_wtf import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms.fields.html5 import DateField
from wtforms.fields import SelectField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class FormCandidateReg(Form):
    username = TextField(
        'username',
        validators=[
            validators.DataRequired(),
            validators.Length(min=4, message='Choose a username of at least 4 characters')
        ]
    )

    password = PasswordField(
        'password',
        validators=[
            validators.DataRequired(),
            validators.Length(min=8, message='Choose a password of at least 8 characters')
        ]
    )

    passwordre = PasswordField(
        'passwordre',
        validators=[
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match')
        ]
    )

    first_name = TextField(
        'first_name',
        validators=[
            validators.DataRequired()
        ]
    )

    last_name = TextField(
        'last_name',
        validators=[
            validators.DataRequired()
        ]
    )

    dob = DateField(
        'dob',
        validators=[
            validators.DataRequired()
        ]
    )

    gender = SelectField(
        'gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        validators=[
            validators.DataRequired()
        ]
    )

    standard = SelectField(
        'standard',
        choices=[(str(x), str(x)) for x in range(1, 13)],
        validators=[
            validators.DataRequired()
        ]
    )

    school = TextField(
        'school',
        validators=[
            validators.DataRequired()
        ]
    )

    email = EmailField(
        'email',
        validators=[
            validators.DataRequired(),
            validators.Email()
        ]
    )

    phone = TextField(
        'phone',
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