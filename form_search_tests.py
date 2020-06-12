
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import PasswordField
from wtforms.fields.html5 import DateField
from wtforms.fields import SelectField
from wtforms import SubmitField
from wtforms import validators

import constants

class FormSearchTests(FlaskForm):

    title = TextField(
        'Title',
        validators=[
        ]
    )

    subject = SelectField(
        'Subject',
        choices=constants.choices(),
        validators=[

        ]
    )

    date = DateField(
        'Date',
        validators=[

        ]
    )

    submit = SubmitField(
        'Search',
        validators=[

        ]
    )

