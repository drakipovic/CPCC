from main import db


class User(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(40))
	name = db.Column(db.String(50))
	surname = db.Column(db.String(200))
	e_mail = db.Column(db.String(50))
	country = db.Column(db.String(50))

	def __init__(self, username, password, name, surname, e_mail, country):
		self.username = username
		self.password = password
		self.name = name
		self.surname = surname
		self.e_mail = e_mail
		self.country = country

	def __repr__(self):
		return 'User(%r, %r)' % (self.username, self.e_mail)

	def save(self):
		db.session.add(self)
		db.session.commit()


class Task(db.Model):
	__tablename__ = 'tasks'

	task_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	text = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	user = db.relationship('User', backref=db.backref('tasks', lazy='dynamic'))
	#contests = db.relationship('Contest', secondary=contest_task, back_populates='tasks')

	def __init__(self, name, text, user):
		self.name = name
		self.text = text
		self.user = user

	def __repr__(self):
		return 'Task(%r)' % (self.name)

	def save(self):
		db.session.add(self)
		db.session.commit()


class Contest(db.Model):
	__tablename__ = 'contests'

	contest_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	time = db.Column(db.DateTime())
	duration = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	user = db.relationship('User', backref=db.backref('contests', lazy='dynamic'))
	#tasks = db.relationship('Task', secondary=contest_task, back_populates='contests')

	def __init__(self, name, time, duration, user, tasks):
		self.name = name
		self.time = time
		self.duration = duration
		self.user = user
		self.tasks = tasks

	def __repr__(self):
		return 'Contest(%r)' % (self.name)

	def save(self):
		db.session.add(self)
		db.session.commit()
		for task_id in self.tasks:
			contest_task = Contest_Task(self.contest_id, task_id)
			contest_task.save()


class Contest_Task(db.Model):
	__tablename__ = 'contest_tasks'

	contest_id = db.Column(db.Integer, primary_key=True)
	task_id = db.Column(db.Integer, primary_key=True)

	def __init__(self, contest_id, task_id):
		self.contest_id = contest_id
		self.task_id = task_id

	def __repr__(self):
		return 'Contest_Task(%r, %r)' % (self.contest_id, self.task_id)

	def save(self):
		db.session.add(self)
		db.session.commit()