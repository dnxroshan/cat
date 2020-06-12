
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.fields import DecimalField
from wtforms.fields import SelectField
from wtforms.fields import TextAreaField
from wtforms.fields import FileField
from wtforms.fields.html5 import DateField
from wtforms import SubmitField
from wtforms import validators

import constants

class FormAddTest(FlaskForm):
    title = TextField(
        'title',
        validators=[
            validators.DataRequired()
        ]
    )

    description = TextAreaField(
        'description',
        validators=[
            validators.DataRequired()
        ]
    )

    date = DateField(
        'date',
        validators=[
            validators.DataRequired()
        ]
    )

    subject = SelectField(
        'subject',
        choices=list(zip(constants.SUBJECTS, constants.SUBJECTS)),
        validators=[
            validators.DataRequired()
        ]
    )

    standard = SelectField(
        'standard',
        validators=[
            validators.DataRequired()
        ]
    )

    score_easy = DecimalField(
        'score_easy',
        validators=[
            validators.DataRequired()
        ]
    )

    score_medium = DecimalField(
        'score_medium',
        validators=[
            validators.DataRequired()
        ]
    )

    score_hard = DecimalField(
        'score_hard',
        validators=[
            validators.DataRequired()
        ]
    )

    score_threshold = DecimalField(
        'score_threshold',
        validators=[
            validators.DataRequired()
        ]
    )

    question_bank = FileField(
        'question_bank',
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

