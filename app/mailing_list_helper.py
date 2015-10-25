from app import app
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer


def generate_token(email, salt):
    """ Generates and returns a token based on the email address and salt.

    :param email: the email address used for token generation
    :type email: str
    :param salt: the salt used for token generation
    :type salt: str

    :return: str
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=None):
    """ Confirms token. Returns email address on success, or an empty string on failure.

    :param token: the token to be confirmed
    :type token: str
    :param salt: the salt that was used for the token generation
    :type salt: str
    :param expiration: the expiration of the token in seconds
    :type expiration: int

    :return: str
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except:
        return ''
    return email


def send_confirmation_email(mail, user, url):
    """ Sends the confirmation email

    :param mail: the flask-mail object
    :type mail: flask.ext.mail.Mail
    :param user: the recepient of the email
    :type user: app.models.User
    :param url: the URL for the confirmation link
    :type url: str
    """
    msg = Message(
        sender=('CoderDojo Dallas', 'coderdojodallas@gmail.com'),
        recipients=[user.email],
        subject='Please confirm your email subscription for CoderDojo Dallas',
        html='<a href="{0}">Click here to confirm your email subscription to CoderDojo Dallas.</a>'.format(url)
    )
    mail.send(msg)
