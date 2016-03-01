from flask import render_template, session, request, redirect

from main import app
from models import User


@app.before_request
def _before_request():
	if 'register' in request.url:
		return

	if 'login' in request.url and request.method == 'GET':
		return

	if 'logged_in' not in session and 'login' not in request.url:
		return redirect('/login')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', username=session['logged_in'])


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