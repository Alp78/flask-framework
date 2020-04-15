import smtplib
from flask import render_template
from config import app, MAIL_USERNAME, MAIL_PASSWORD, mail
from threading import Thread
from flask_mail import Message
from models import User

def sendMail(subjectLine, emailBody):
    with app.app_context():
        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.ehlo()  # identifies user to the SMTP server
            server_ssl.login(MAIL_USERNAME, MAIL_PASSWORD)
            sent_from = '{}@xxx.com'.format('no-reply')
            sent_to = ['peringer@google.com']

            msg = 'Subject: {}\n\n{}'.format(subjectLine, emailBody)

            server_ssl.sendmail(sent_from, sent_to, msg)
        except:
            print('Error while connecting to Gmail SMTP server.')

def sendAsyncMail(subjectLine, emailBody):
    Thread(target=sendMail, args=(subjectLine, emailBody)).start()

def sendFlaskMail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print(user.username)
    print(user.email)
    sendFlaskMail('[Live Dictionary] Reset Your Password',
               sender=['', ''],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
