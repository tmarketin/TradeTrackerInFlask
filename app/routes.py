from app import appInstance, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@appInstance.route('/')
@appInstance.route('/index')
@login_required
def index():
    people = [{
        'name': 'Edward Teller',
        'field': 'Nuclear Physics',
        'country': 'Hungary'
    },
    {
        'name': 'Stanislaw Ulam',
        'field': 'Mathematics',
        'country': 'Austria-Hungary'
    }
    ]
    return render_template('index.html', title="Home", people=people)

@appInstance.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formInstance  = LoginForm()
    if formInstance.validate_on_submit():
        user = User.query.filter_by(username = formInstance.username.data).first()
        if user is None or not user.check_password(formInstance.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = formInstance.rememberMe.data)
        nextPage = request.args.get('next')
        if not nextPage or url_parse(nextPage).netloc != '':
            return redirect(url_for('index'))
        return redirect(nextPage)
    return render_template('login.html', title = 'Sign In', form = formInstance)

@appInstance.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@appInstance.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formInstance = RegistrationForm()
    if formInstance.validate_on_submit():
        newUser = User(username = formInstance.username.data, email = formInstance.email.data)
        newUser.set_password(formInstance.password.data)
        db.session.add(newUser)
        db.session.commit()
        flash('Congratulations, registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = formInstance)

@appInstance.route('/jsontest')
@login_required
def jsonTest():
    people = {
        'name': 'Edward Teller',
        'field': 'Nuclear Physics',
        'country': 'Hungary'
    }

    return people