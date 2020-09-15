from app import appInstance
from flask import render_template

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

@appInstance.route('/jsontest')
def jsonTest():
    people = {
        'name': 'Edward Teller',
        'field': 'Nuclear Physics',
        'country': 'Hungary'
    }

    return people