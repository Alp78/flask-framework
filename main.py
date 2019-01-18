from flask import Flask, render_template, make_response, flash, redirect, url_for, request
from werkzeug.urls import url_parse
import liveserver
from config import app
from models import db, User, Dictionary
from forms import LoginForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from forms import RegistrationForm
from datetime import datetime
import logging
from logging.handlers import SMTPHandler
from emailbot import sendMail


# imports for "flask shell" interactive python
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dictionary': Dictionary}


# records last seen
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # checks if username already exists
        if db.session.query(User).filter_by(username=form.username.data).first():
            subjectLine = 'Another user tried to pick an existing username'
            emailBody = 'User {} - Edit Profile Error: Existing User {}'.format(current_user.username, form.username.data)
            sendMail(subjectLine, emailBody)
            
            """
            init_email_error_handler(app, 'User {} - Edit Profile Error: Existing User {}'
            .format(current_user.username, form.username.data))
            
            app.logger.error('User {} tried to change their username to an existing one: {}'
            .format(current_user.username, form.username.data))
            """

            return render_template("500.html"), 500
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# landing page
@app.route('/')
@login_required
def welcome():
    resp = make_response(render_template('welcome.html'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route('/index')
@login_required
def index():
    return render_template('base.html')

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    dictionaries = [
        {'author': user, 'dict_name': 'Dictionary #1'},
        {'author': user, 'dict_name': 'Dictionary #2'}
    ]
    return render_template('user.html', user=user, dictionaries=dictionaries)


"""
def init_email_error_handler(app, subjectLine):

    if app.debug: return "App in Debug mode!"  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = MAIL_SERVER
    port = MAIL_PORT
    from_addr = MAIL_DEFAULT_SENDER
    username = MAIL_USERNAME
    password = MAIL_PASSWORD
    secure = () if MAIL_USE_TLS else None


    # Retrieve app settings from app.config
    to_addr_list = ADMINS
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', subjectLine)

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message') 
"""



if __name__ == '__main__':
    liveserver.serve(app)
