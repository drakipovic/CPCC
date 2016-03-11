from wtforms import Form, TextAreaField, TextField, validators, DateTimeField

class TaskForm(Form):
	task_name = TextField('Task Name', [validators.Required()])
	task_text = TextAreaField('Task Text')


class ContestForm(Form):
	contest_name = TextField('Contest Name', [validators.Required()])
	contest_start = DateTimeField('Contest Start')