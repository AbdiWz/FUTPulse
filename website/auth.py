from . import db 
from .models import User
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

def not_logged_in_required(view_func):
	@wraps(view_func)
	def decorated_function(*args, **kwargs):
		if current_user.is_authenticated:
			flash('You are already logged in.', 'info')
			return redirect(url_for('dashboard')) 
		return view_func(*args, **kwargs)
	return decorated_function

@auth.route('/login', methods=['GET','POST']) 
@not_logged_in_required
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		#Query User
		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Logged in successfully!', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password, try again.', category='error')
		else:
			flash('Email does not exist.', category='error')
	return render_template("login.html")

@auth.route('/logout')
@login_required 
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

def checks(first_name, email, password1, password2): 
	if len(email) < 4:
		flash('Email must be greater than 4 characters.', category='error')
		return True
	elif len(first_name) < 2:
		flash('First Name must be greater than 2 characters.', category='error')
		return True
	elif password1 != password2:
		flash('Passwords dont match.', category='error')
		return True
	elif len(password1) < 7:
		flash('Password must be greater than 7 characters.', category='error')
		return True
	else:
		return False

@auth.route('/sign-up', methods=['GET','POST'])
@not_logged_in_required
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('FirstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		#Query Email
		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists', category='error')
		errors = checks(first_name, email, password1, password2)        
		#Add User
		if errors is False:
			new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			flash('Account Created.', category='success')
			return redirect(url_for('views.home'))
	return render_template("sign-up.html")