from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, PasswordField


class indexForm(Form):
    title = StringField('view to -do title',
                        [validators.Required(message='view the title!')])
    desc = StringField('view to-do description',
                       [validators.Required(message='view something!')])
    submit = SubmitField('Submit')


class todoForm(Form):
    title = StringField('add to -do title',
                        [validators.Required(message='Create a title!')])
    desc = StringField('add to-do description',
                       [validators.Required(message='Do something!')])
    submit = SubmitField('Submit')


class loginForm(Form):
    username = StringField(validators.Required(message='Enter username'))

    password = PasswordField(validators.Required(message='Enter password'))

    submit = SubmitField('Submit')
