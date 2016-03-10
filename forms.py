from wtforms import Form, TextAreaField, TextField, validators, DateField

class TaskForm(Form):
	task_name = TextField('Task Name', [validators.Required()])
	task_text = TextAreaField('Task Text')


class ContestForm(Form):
	contest_name = TextField('Contest Name', [validators.Required()])
	contest_start = DateField('Contest Start')