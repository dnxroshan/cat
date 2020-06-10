
from flask_wtf import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms.fields.html5 import DateField
from wtforms.fields import SelectField
from wtforms import SubmitField
from wtforms import validators

import constants

class FormSearchTests(Form):

    title = TextField(
        'Title',
        validators=[
            validators
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

