import pycountry
from wtforms import TextAreaField, TextField, validators, DateTimeField, IntegerField, SelectMultipleField, SelectField, PasswordField
from flask_wtf.file import FileField, FileRequired
from flask.ext.wtf import Form

from models import Task, User


class Unique(object):
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'Already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise validators.ValidationError(self.message)


class MemberForm(Form):
    username = TextField('Username', [validators.Required(), Unique(User, User.username)])
    password = PasswordField('Password', [validators.Required()])
    name = TextField('Name', [validators.Required()])
    surname = TextField('Surname', [validators.Required()])
    e_mail = TextField('Email', [validators.Required()])
    country = SelectField('Country', [validators.Required()], choices=[(country.name, country.alpha2) for country in pycountry.countries])


class TaskForm(Form):
    name = TextField('Name', [validators.Required()])
    time_limit = IntegerField('Time limit')
    memory = IntegerField('Memory')
    text = TextAreaField('Text')


class ContestForm(Form):
    name = TextField('Name', [validators.Required()])
    start = DateTimeField('Start')
    duration = SelectField('Duration', choices=[(i, str(i)+'h') for i in range(1, 24+1)], coerce=int)


class SelectTasksForm(Form):
    tasks = SelectMultipleField('Tasks', coerce=int)


class SourceCodeSubmitForm(Form):
    source_code = FileField('SourceCode', validators=[FileRequired()])


class InviteForm(Form):
    users = SelectMultipleField('Users', coerce=int)
    

