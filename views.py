from flask import render_template, session, request, redirect, g, url_for

from main import app
from models import User, Task, Contest


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
	return render_template('home.html', username=g.user.username)


@app.route('/profile/<username>')
def profile(username):
	user = User.query.filter_by(username=username).first()
	return render_template('profile.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['Username']
		password = request.form['Password']
		user = User.query.filter_by(username=username, password=password).first()
		if user is None:
			return redirect('/login')
		else:
			session['logged_in'] = username
			return redirect('/home')
	
	return render_template('login.html')


@app.route('/tasks/<username>')
def user_tasks(username):
	user = User.query.filter_by(username=username).first()
	tasks = Task.query.filter_by(user_id=user.user_id).all()
	return render_template('user_tasks.html', tasks=tasks)


@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
	if request.method == 'POST':
		task_name = request.form['TaskName']
		task_text = request.form['TaskText']
		task = Task(task_name, task_text, g.user)
		task.save()
		return redirect(url_for('task', task_id=task.task_id))

	return render_template('task_form.html')


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
	if request.method == 'POST': 
		#contest_name = request.form['ContestName']
		#contest_time = request.form['ContestTime']
		#contest_duration = request.form['ContestDuration']
		#contest = Contest(contest_name, contest_time, contest_duration, g.user)
		#contest.save()
		#return redirect(url_for('contest', contest_id=contest.contest_id))
		return render_template('home.html')
	
	return render_template('contest_form.html')



@app.route('/contest/<contest_id>', methods=['GET'])
def contest(contest_id):
	contest = Contest.query.get(contest_id)
	return render_template('contest.html', contest=contest)


@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	return redirect('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['Username']
		password = request.form['Password']
		name = request.form['Name']
		surname = request.form['Surname']
		e_mail = request.form['EMail']
		country = request.form['Country']
		user = User(username, password, name, surname, e_mail, country)
		user.save()
		return redirect('/login')

	return render_template('register.html')
