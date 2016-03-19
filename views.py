from flask import render_template, session, request, redirect, g, url_for, flash
import pycountry

from main import app
from models import User, Task, Contest, Friendship, ContestNotification
from forms import TaskForm, ContestForm, MemberForm, InviteForm


@app.before_request
def _before_request():
	if session.get('logged_in'):
		username = session['logged_in']
		g.user = User.query.filter_by(username=username).first()
		return

	if 'register' in request.url:
		return

	if 'login' in request.url and request.method == 'GET':
		return

	if 'logged_in' not in session and 'login' not in request.url:
		flash("You have to login to see this content!", 'danger')
		return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/profile')
def profile():
	user = g.user
	friendships = Friendship.query.filter_by(user_id=user.user_id).all()
	friends = [User.query.get(f.friend_id) for f in friendships]
	tasks = Task.query.filter_by(author_id=user.user_id).all()
	contests = Contest.query.filter_by(author_id=user.user_id).all()
	country_code = pycountry.countries.get(name=user.country).alpha2.lower()
	if user.username == 'katarina': country_code='rm'
	return render_template('my_profile.html', user=user, tasks=tasks, contests=contests, country=user.country, country_code=country_code, friends=friends)


@app.route('/compete')
def compete(): 
	contests = [Contest.query.get(contest.contest_id) for contest in g.user.contests]
	return render_template('compete.html', contests=contests)


@app.route('/profile/<username>')
def other_profile(username):
	if username == g.user.username:
		return redirect('/profile')

	other_user = User.query.filter_by(username=username).first()
	if other_user == None: 
		return redirect('/home')

	user = g.user
	my_friendships = Friendship.query.filter_by(user_id=user.user_id).all()
	my_friends = [User.query.get(f.friend_id) for f in my_friendships]

	is_friend = False
	if other_user in my_friends:
		is_friend = True

	friendships = Friendship.query.filter_by(user_id=other_user.user_id).all()
	friends = [User.query.get(f.friend_id) for f in friendships]
	country_code = pycountry.countries.get(name=other_user.country).alpha2.lower()
	if username == 'katarina': country_code='rm'
	return render_template('other_profile.html', user=g.user, other_user=other_user, country=other_user.country,
							country_code=country_code, friends=friends, is_friend=is_friend)


@app.route('/add_friend/<friend_id>')
def add_friend(friend_id):
	user = g.user
	user.add_friend(friend_id)
	friend_username = User.query.filter_by(user_id=friend_id).first().username
	return redirect('/profile/' + friend_username)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['inputUsername']
		password = request.form['inputPassword']
		user = User.query.filter_by(username=username, password=password).first()
		if user is None:
			flash("Warning! Wrong username or password.", 'danger')
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
		flash('You were succesfully registered. Please login.', 'success')
		return redirect('/login')

	return render_template('register.html', form=member_form)


@app.route('/tasks/<username>')
def user_tasks(username):
	user = User.query.filter_by(username=username).first()
	tasks = Task.query.filter_by(author_id=user.user_id).all()
	return render_template('user_tasks.html', tasks=tasks)


@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
	form = TaskForm(request.form)
	if request.method == 'POST' and form.validate():
		task = Task(form.name.data, form.text.data, g.user)
		task.save()
		return redirect(url_for('task', task_id=task.task_id))

	return render_template('task_form.html', form=form)


@app.route('/task/<int:task_id>', methods=['GET'])
def task(task_id):
	task = Task.query.get(task_id)
	if task == None:
		return "Nema tog zadatka"
	return render_template('task.html', user=g.user, task=task)


@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
	task = Task.query.get(task_id)
	if g.user.user_id != task.author_id:
		flash('You do not have proper authorization to do this!', 'danger')
		return redirect('/task/' + str(task_id))

	form = TaskForm(obj=task)
	if request.method == 'POST' and form.validate():
		form = TaskForm(request.form)
		form.populate_obj(task)
		task.save()
		return redirect(url_for('task', task_id=task.task_id))

	return render_template('task_form.html', form=form, edit=True)


@app.route('/contests/<username>')
def user_contests(username):
	user = User.query.filter_by(username=username).first()
	contests = Contest.query.filter_by(author_id=user.user_id).all()
	return render_template('user_contests.html', contests=contests)


@app.route('/contest/new', methods=['GET', 'POST'])
def new_contest():
	form = ContestForm(request.form)
	user = g.user
	tasks = Task.query.filter_by(author_id=user.user_id).all()
	form.tasks.choices = [(task.task_id, task.name) for task in tasks]

	if request.method == 'POST' and form.validate():
		tasks = [Task.query.get(task_id) for task_id in form.tasks.data]
		contest = Contest(form.name.data, form.start.data, form.duration.data, user.user_id, tasks)
		contest.save()
		return redirect(url_for('contest', contest_id=contest.contest_id))
	
	return render_template('contest_form.html', form=form)


@app.route('/contest/<int:contest_id>')
def contest(contest_id):
	contest = Contest.query.get(contest_id)
	author = User.query.get(contest.author_id)
	return render_template('contest.html', contest=contest, user=g.user, author=author)


@app.route('/contest/<int:contest_id>/invite', methods=['GET', 'POST'])
def contest_invite(contest_id):
	contest = Contest.query.get(contest_id)
	if g.user.user_id != contest.author_id:
		flash('You do not have proper authorization to do this!', 'danger')
		return redirect('/contest/' + str(contest_id))

	form = InviteForm(obj=contest)
	friendships = Friendship.query.filter_by(user_id=g.user.user_id).all()
	users = [User.query.get(friendship.friend_id) for friendship in friendships]
	form.users.choices = [(user.user_id, user.username) for user in users]

	if request.method == 'POST' and form.validate():
		form = InviteForm(request.form)
		users = [User.query.get(user_id) for user_id in form.users.data]
		form.users.data = users
		form.populate_obj(contest)
		contest.save()
		return redirect(url_for('contest', contest_id=contest.contest_id))

	return render_template('invite_form.html', form=form, edit=True)


@app.route('/contest/<int:contest_id>/edit', methods=['GET', 'POST'])
def edit_contest(contest_id):
	contest = Contest.query.get(contest_id)
	if g.user.user_id != contest.author_id:
		flash('You do not have proper authorization to do this!', 'danger')
		return redirect('/contest/' + str(contest_id))

	form = ContestForm(obj=contest)
	tasks = Task.query.filter_by(author_id=g.user.user_id).all()
	form.tasks.choices = [(task.task_id, task.name) for task in tasks]

	if request.method == 'POST' and form.validate():
		form = ContestForm(request.form)
		tasks = [Task.query.get(task_id) for task_id in form.tasks.data]
		form.tasks.data = tasks
		form.populate_obj(contest)
		contest.save()
		return redirect(url_for('contest', contest_id=contest.contest_id))

	return render_template('contest_form.html', form=form, edit=True)


@app.route('/search/<search_query>')
def search(search_query):
	tasks = Task.query.filter(Task.name.contains(search_query)).all()
	users = User.query.filter(User.username.contains(search_query)).all()
	contests = Contest.query.filter(Contest.name.contains(search_query)).all()
	return render_template('search_results.html', tasks=tasks, users=users, contests=contests)


@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	return redirect('login')