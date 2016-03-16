import pycountry
from wtforms import Form, TextAreaField, TextField, validators, DateTimeField, IntegerField, SelectMultipleField, SelectField, PasswordField
from models import Task

class MemberForm(Form):
	username = TextField('Username', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])
	name = TextField('Name', [validators.Required()])
	surname = TextField('Surname', [validators.Required()])
	e_mail = TextField('Email', [validators.Required()])
	country = SelectField('Country', [validators.Required()], choices=[(country.name, country.alpha2) for country in pycountry.countries])


class TaskForm(Form):
	name = TextField('Name', [validators.Required()])
	text = TextAreaField('Text')


class ContestForm(Form):
	name = TextField('Name', [validators.Required()])
	start = DateTimeField('Start')
	duration = SelectField('Duration', choices=[(i, str(i)+'h') for i in range(1, 24)], coerce=int)
	tasks = SelectMultipleField('Tasks', coerce=int)


class InviteForm(Form):
	users = SelectMultipleField('Users', coerce=int)