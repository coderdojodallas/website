from app import app
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer


def confirm_token(token, salt, expiration=0):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except:
        return False
    return email


def generate_token(email, salt):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def send_confirmation_email(mail, user, url):
    msg = Message(
        sender=('CoderDojo Dallas', 'coderdojodallas@gmail.com'),
        recipients=[user.email],
        subject='Please confirm your email subscription for CoderDojo Dallas',
        html='<a href="{0}">Click here to confirm your email subscription to CoderDojo Dallas.</a>'.format(url)
    )
    mail.send(msg)
