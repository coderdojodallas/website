from flask import url_for
from flask.ext.mail import Message
from . import token_services as ts


def send_confirmation_email(email, confirmation_url):
    """ Sends the email to the specified address

    :param str email: The recipient's email address
    :param str conrifmation_url: The confirmation url
    """
    msg = Message(
        sender=('CoderDojo Dallas', 'coderdojodallas@gmail.com'),
        recipients=[email],
        subject='Please confirm your email subscription for CoderDojo Dallas',
        html='<a href="{0}">Click here to confirm your email subscription to CoderDojo Dallas.</a>'.format(url)
    )
    mail.send(msg)
