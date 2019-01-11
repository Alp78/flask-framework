from flask import Flask, render_template, make_response, flash, redirect, url_for, request
from werkzeug.urls import url_parse
import liveserver
from config import app
from models import db, User, Dictionary
from forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

# imports for "flask shell" interactive python
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dictionary': Dictionary}


# landing page
@app.route('/')
@login_required
def welcome():
    resp = make_response(render_template('welcome.html', title='Welcome'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route('/index')
@login_required
def index():
    return "Hello, World"

# login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    liveserver.serve(app)
