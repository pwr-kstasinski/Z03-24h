from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    """ Login form """
    username = StringField('username',
                           validators=[
                               InputRequired(message="Username required")
                           ])
    password = PasswordField('password',
                             validators=[
                                 InputRequired(message="Password required")
                             ])
    submit_button = SubmitField('NEXT')


class RegistrationForm(FlaskForm):
    """ Registration form """
    username = StringField('username',
                           validators=[
                               InputRequired(message="Username required"),
                               Length(min=4, max=25, message="Username must be between 4 and 25 characters")
                           ])

    password = PasswordField('password', validators=[
        InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25 characters")
    ])
    confirm_password = PasswordField('confirm_password', validators=[
        InputRequired(message="Username required"),
        EqualTo('password', message="Password must match")
    ])
    submit_button = SubmitField('NEXT')


class ChatForm(FlaskForm):
    """ Chat form """
    user = StringField('user',
                       validators=[
                           InputRequired(message="Username required")
                       ])
    submit_button = SubmitField('ADD CHAT')


class MsgForm(FlaskForm):
    """ Messages form """
    msg = StringField('msg',
                      validators=[
                          InputRequired(message="Username required")
                      ])
    submit_button = SubmitField('SEND')
