from app import app
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['EMAIL_CONFIRMATION_SALT'])


def confirm_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET-KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['EMAIL_CONFIRMATION_SALT'],
            max_age=app.config['EMAIL_CONFIRMATION_EXPIRATION']
        )
    except:
        return False
    return email


def send_confirmation_email(mail, recipient, url):
    msg = Message(
        sender=('CoderDojo Dallas', "info@coderdojodallas.com"),
        recipients=[recipient],
        subject='Please confirm your email subscription for CoderDojo Dallas',
        html='<a href="{0}">Click here to confirm your email subscription to CoderDojo Dallas.</a>'.format(url)
    )
    mail.send(msg)
