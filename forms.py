from wtforms import Form, TextAreaField, TextField, validators, DateTimeField, IntegerField, SelectMultipleField, SelectField


class TaskForm(Form):
	task_name = TextField('Name', [validators.Required()])
	task_text = TextAreaField('Text')


class ContestForm(Form):
	contest_name = TextField('Name', [validators.Required()])
	contest_start = DateTimeField('Start')
	contest_duration = SelectField('Duration', choices=[(i, str(i)+'h') for i in range(1, 24)], coerce=int)
	contest_tasks = SelectMultipleField('Tasks', coerce=int)
