from wtforms import Form, TextAreaField, TextField, validators, DateTimeField, IntegerField, SelectMultipleField


class TaskForm(Form):
	task_name = TextField('Name', [validators.Required()])
	task_text = TextAreaField('Text')


class ContestForm(Form):
	contest_name = TextField('Name', [validators.Required()])
	contest_start = DateTimeField('Start')
	contest_duration = IntegerField('Duration', [validators.Required()])
	contest_tasks = SelectMultipleField('Tasks')
