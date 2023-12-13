from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from sqlalchemy.exc import IntegrityError
from website import db
from website.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('views.home'))

        flash('Invalid username or password')

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            flash('Passwords do not match')
            return redirect(url_for('auth.signup'))

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            flash('Username already exists')
            return redirect(url_for('auth.signup'))

        if existing_user_email:
            flash('Email address already exists. Please choose a different email.')
            return redirect(url_for('auth.signup'))

        new_user = User(
            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname,
            gender=gender
        )
        new_user.set_password(password1)

        new_profile_picture = request.files.get('profile_picture')
        if new_profile_picture:
            try:
                new_user.save_profile_picture(new_profile_picture, current_app.config['UPLOAD_FOLDER'])
            except ValueError as e:
                flash(str(e))
                return redirect(url_for('auth.signup'))

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('auth.login'))

        except IntegrityError as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/unauthorized')
def unauthorized():
    flash('You need to be logged in to access this page.')
    return redirect(url_for('auth.login'))