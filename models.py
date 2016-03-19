from main import db

contest_users = db.Table('contest_users', 
											db.Column('contest_id', db.Integer, db.ForeignKey('contests.contest_id'), primary_key=True),
											db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)


class User(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(40))
	name = db.Column(db.String(50))
	surname = db.Column(db.String(200))
	e_mail = db.Column(db.String(50))
	country = db.Column(db.String(50))
	
	contests = db.relationship('Contest', secondary=contest_users, lazy='dynamic')

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

	def add_friend(self, friend_id):
		friendship = Friendship(self.user_id, friend_id)
		friendship.save()


class Friendship(db.Model):
	__tablename__ = 'friendships'

	user_id = db.Column(db.Integer, primary_key=True)
	friend_id = db.Column(db.Integer, primary_key=True)

	def __init__(self, user_id, friend_id):
		self.user_id = user_id
		self.friend_id = friend_id

	def __repr__(self):
		return 'Friendship(%r, %r)' % (self.user_id, self.friend_id)

	def save(self):
		db.session.add(self)
		db.session.commit()


contest_tasks = db.Table('contest_tasks', 
											db.Column('contest_id', db.Integer, db.ForeignKey('contests.contest_id')),
											db.Column('task_id', db.Integer, db.ForeignKey('tasks.task_id'))
)


class Task(db.Model):
	__tablename__ = 'tasks'

	task_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	text = db.Column(db.Text)
	author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	author = db.relationship('User', backref='tasks')

	def __init__(self, name, text, author):
		self.name = name
		self.text = text
		self.author = author

	def __repr__(self):
		return 'Task(%r)' % (self.name)

	def save(self):
		db.session.add(self)
		db.session.commit()


class Contest(db.Model):
	__tablename__ = 'contests'

	contest_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	start = db.Column(db.DateTime())
	duration = db.Column(db.Integer)
	author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	tasks = db.relationship('Task', secondary=contest_tasks, lazy='dynamic')
	users = db.relationship('User', secondary=contest_users, lazy='dynamic')

	def __init__(self, name, start, duration, author_id):
		self.name = name
		self.start = start
		self.duration = duration
		self.author_id = author_id

	def __repr__(self):
		return 'Contest(%r)' % (self.name)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def set_tasks(self, tasks):
		self.tasks = tasks