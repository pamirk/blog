from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Pamirkhan'}
    posts = [
        {
            'author': {'username': 'Pamir'},
            'body': 'Beautiful day in Quetta!'
        },
        {
            'author': {'username': 'khan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
