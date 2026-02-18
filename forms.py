from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):

    email = EmailField(
        "Your Email",
        validators=[DataRequired(), Email()]
    )
    subject = StringField(
        "Subject",
        validators=[DataRequired()]
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired()]
    )
    submit = SubmitField("Send message")