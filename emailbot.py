import smtplib
from config import MAIL_USERNAME, MAIL_PASSWORD

def sendMail(subjectLine, emailBody):
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