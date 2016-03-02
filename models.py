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


contest_tasks = db.Table('contest_tasks', db.Model.metadata,
	db.Column('contest_id', db.ForeignKey('tasks.task_id'), primary_key=True),
	db.Column('task_id', db.ForeignKey('contests.contest_id'), primary_key=True))


class Task(db.Model):
	__tablename__ = 'tasks'

	task_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	text = db.Column(db.Text)

	contests = db.relationship('Contest', secondary=contest_tasks, back_populates='tasks')

	def __init__(self, name, text):
		self.name = name
		self.text = text

	def __repr__(self):
		return 'Task(%r)' % self.name 

	def save(self):
		db.session.add(self)
		db.session.commit()


class Contest(db.Model):
	__tablename__ = 'contests'

	contest_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	time = db.Column(db.DateTime())

	tasks = db.relationship('Task', secondary=contest_tasks, back_populates='contests')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return 'Contest(%r)' % self.name

	def save(self):
		db.session.add(self)
		db.session.commit()