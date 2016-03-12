import pycountry
from wtforms import Form, TextAreaField, TextField, validators, DateTimeField, IntegerField, SelectMultipleField, SelectField, PasswordField


class MemberForm(Form):
	username = TextField('Username', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])
	name = TextField('Name', [validators.Required()])
	surname = TextField('Surname', [validators.Required()])
	e_mail = TextField('Email', [validators.Required()])
	country = SelectField('Country', [validators.Required()], choices=[(country.name, country.alpha2) for country in pycountry.countries])


class TaskForm(Form):
	task_name = TextField('Name', [validators.Required()])
	task_text = TextAreaField('Text')


class ContestForm(Form):
	contest_name = TextField('Name', [validators.Required()])
	contest_start = DateTimeField('Start')
	contest_duration = SelectField('Duration', choices=[(i, str(i)+'h') for i in range(1, 24)], coerce=int)
	contest_tasks = SelectMultipleField('Tasks', coerce=int)
