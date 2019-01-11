from flask import Flask, render_template, make_response, flash, redirect, url_for
import liveserver
from config import *
from models import *
from forms import LoginForm

# imports for "flask shell" interactive python
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dictionary': Dictionary}


# landing page
@app.route('/')
def welcome():
    resp = make_response(render_template('welcome.html'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route('/index')
def index():
    return "Hello, World"

# login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    liveserver.serve(app)
