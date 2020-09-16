from app import appInstance
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@appInstance.route('/')
@appInstance.route('/index')
def index():
    user = {'username': 'Tomislav'}
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
    formInstance  = LoginForm()
    if formInstance.validate_on_submit():
        flash('Login requested for user {}, rememberMe = {}'.format(
            formInstance.username.data, formInstance.rememberMe.data)
            )
        return redirect(url_for('index'))

    return render_template('login.html', title = 'Sign In', form = formInstance)

@appInstance.route('/jsontest')
def jsonTest():
    people = {
        'name': 'Edward Teller',
        'field': 'Nuclear Physics',
        'country': 'Hungary'
    }

    return people