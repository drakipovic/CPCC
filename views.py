from flask import render_template, session, request, redirect, g, url_for
import pycountry

from main import app
from models import User, Task, Contest, Contest_Task, Friendship
from forms import TaskForm, ContestForm, MemberForm


@app.before_request
def _before_request():
	if session.get('logged_in'):
		username = session['logged_in']
		g.user = User.query.filter_by(username=username).first()

	if 'register' in request.url:
		return

	if 'login' in request.url and request.method == 'GET':
		return

	if 'logged_in' not in session and 'login' not in request.url:
		return redirect('/login')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/profile')
def profile():
	user = g.user
	username = user.username
	friendships = Friendship.query.filter_by(user_id=user.user_id).all()
	friends = [User.query.get(f.friend_id) for f in friendships]
	tasks = Task.query.filter_by(user_id=user.user_id).all()
	contests = Contest.query.filter_by(user_id=user.user_id).all()
	country_code = pycountry.countries.get(name=user.country).alpha2.lower()
	return render_template('profile.html', user=user, tasks=tasks, contests=contests, country=user.country, country_code=country_code, friends=friends)


@app.route('/profile/<username>')
def user(username):
	if username == g.user.username:
		return redirect('/profile')
	user = User.query.filter_by(username=username).first()
	if user == None: 
		return redirect('/home')
	return render_template('user.html', user=user)


@app.route('/friend/<friend_id>')
def friend(friend_id):
	user = g.user
	if friend_id == user.user_id:
		return redirect('/profile')
	friendship = Friendship.query.filter_by(user_id=user.user_id, friend_id=friend_id).first()
	if friendship == None:
		user.add_friend(friend_id)
	return redirect('/profile')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['inputUsername']
		password = request.form['inputPassword']
		user = User.query.filter_by(username=username, password=password).first()
		if user is None:
			return redirect('/login')
		else:
			session['logged_in'] = username
			return redirect('/home')
	
	return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	member_form = MemberForm(request.form)
	if request.method == 'POST' and member_form.validate():
		username = member_form.username.data
		password = member_form.password.data
		name = member_form.name.data
		surname = member_form.surname.data
		e_mail = member_form.e_mail.data
		country = member_form.country.data
		user = User(username, password, name, surname, e_mail, country)
		user.save()
		return redirect('/login')

	return render_template('register.html', form=member_form)


@app.route('/tasks/<username>')
def user_tasks(username):
	user = User.query.filter_by(username=username).first()
	tasks = Task.query.filter_by(user_id=user.user_id).all()
	return render_template('user_tasks.html', tasks=tasks)


@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
	task_form = TaskForm(request.form)
	if request.method == 'POST' and task_form.validate():
		task = Task(task_form.task_name.data, task_form.task_text.data, g.user)
		task.save()
		return redirect(url_for('task', task_id=task.task_id))

	return render_template('task_form.html', form=task_form)


@app.route('/task/<task_id>', methods=['GET'])
def task(task_id):
	task = Task.query.get(task_id)
	return render_template('task.html', task=task)


@app.route('/contests/<username>')
def user_contests(username):
	user = User.query.filter_by(username=username).first()
	contests = Contest.query.filter_by(user_id=user.user_id).all()
	return render_template('user_contests.html', contests=contests)


@app.route('/contest/new', methods=['GET', 'POST'])
def new_contest():
	contest_form = ContestForm(request.form)
	user = g.user
	tasks = Task.query.filter_by(user_id=user.user_id).all()
	contest_form.contest_tasks.choices = [(task.task_id, task.name) for task in tasks]

	if request.method == 'POST' and contest_form.validate(): 
		contest = Contest(contest_form.contest_name.data, contest_form.contest_start.data, 
							contest_form.contest_duration.data, g.user, contest_form.contest_tasks.data)
		contest.save()
		return redirect(url_for('contest', contest_id=contest.contest_id))
	
	return render_template('contest_form.html', form=contest_form)


@app.route('/contest/<contest_id>', methods=['GET'])
def contest(contest_id):
	contest = Contest.query.get(contest_id)
	contest_tasks = Contest_Task.query.filter_by(contest_id=contest_id).all()
	tasks = [Task.query.get(contest_task.task_id) for contest_task in contest_tasks]
	return render_template('contest.html', contest=contest, tasks=tasks)


@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	return redirect('login')
