from . import mail, db
from flask import render_template, current_app
from flask_mail import Message
from psycopg2 import connect
from threading import Thread


def async_send_mail(app, msg):
    with app.app_context():
        return mail.send(msg)

def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients= [recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[current_app._get_current_object(), msg])
    thr.start()
    return thr

def create_db():
    message = ''
    try:
        with connect(user='victors', password='victor77', host='localhost') as connection:
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(f'CREATE DATABASE flask_db')
            message = f'DB "flask_db" created...'
    except Exception as error:
        message = f'!!! {error}'
    db.create_all()
    return message    

