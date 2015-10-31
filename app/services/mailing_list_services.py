from app import app, db, mail, messages
from app.models import User
from flask import flash, url_for
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer
from . import token_services as ts


class InvalidUserError(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return "There is no user registered with the email '{0}'".format(self.email)


def add_user(form):
    """ Adds user to mailing list

    :param form: the MailingListForm object
    :type form: app.forms.MailingListForm
    """
    try:
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            if user.confirmed:
                flash(
                    messages.email_address_submitted_and_confirmed(email),
                    'alert-info'
                )
            else:
                flash(
                    messages.email_address_submitted_not_confirmed(email),
                    'alert-info'
                )
        else:
            user = form.create_user()
            db.session.add(user)

            send_confirmation_email(user)

            db.session.commit()
            flash(
                messages.confirmation_email_sent(email),
                'alert-success'
            )
    except Exception as e:
        db.session.rollback()
        raise e


def confirm_user(user_token):
    """ Confirms user via user_token

    :param user_token: the token for the user
    :type user_token: str
    """
    email = ts.confirm_token(
        user_token,
        salt=app.config['EMAIL_CONFIRMATION_SALT'],
        expiration=app.config['EMAIL_CONFIRMATION_EXPIRATION']
    )
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(messages.confirmation_link_invalid(), 'alert-danger')
        raise ts.InvalidTokenError(user_token)

    if user.confirmed:
        flash(messages.confirmation_link_already_confirmed(email), 'alert-info')
    else:
        user.confirmed = True
        db.session.commit()
        flash(messages.confirmation_link_confirmed(email), 'alert-success')


def edit_user(user_token, form):
    """ Edits user info

    :param user_token: the token for the user
    :type user_token: str
    :param form: the MailingListForm object
    :type form: app.forms.MailingListForm
    """
    email = ts.confirm_token(
        user_token,
        salt=app.config['MAILING_LIST_PREFERENCES_SALT'],
    )
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(messages.mailing_list_preferences_error(), 'alert-danger')
        raise ts.InvalidTokenError(user_token)

    # Fill form with user data on GET, edit user on form submit
    if not form.validate_on_submit():
        form.fill_fields_with_user(user)
        return
    else:
        if not form.data_matches_user(user):
            form.update_user(user)
            if form.email.data != email:
                send_confirmation_email(user)
                user.confirmed = False
                flash(
                    messages.mailing_list_preferences_confirmation_email(user.email),
                    'alert-success'
                )

            try:
                db.session.commit()
                flash(messages.mailing_list_preferences_success(), 'alert-success')
            except Exception as e:
                db.session.rollback()
                raise e


def delete_user(user_token):
    """ Deletes user

    :param user_token: the token for the user
    :type user_token: str
    """
    email = ts.confirm_token(
        user_token,
        salt=app.config['MAILING_LIST_PREFERENCES_SALT'],
    )
    if not email:
        flash(messages.mailing_list_unsubscribe_error(), 'alert-danger')
        raise ts.InvalidExceptionError(user_token)

    user = User.query.filter_by(email=email).first()
    if not user:
        raise InvalidUserError(email)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(messages.mailing_list_unsubscribe_success(), 'alert-success')
    except Exception as e:
        db.session.rollback()
        raise e


def send_confirmation_email(user):
    """ Sends the confirmation email

    :param user: the recepient of the email
    :type user: app.models.User
    """
    token = ts.generate_token(
        user.email,
        app.config['EMAIL_CONFIRMATION_SALT']
    )
    url = url_for('confirm_email', token=token, _external=True)
    msg = Message(
        sender=('CoderDojo Dallas', 'coderdojodallas@gmail.com'),
        recipients=[user.email],
        subject='Please confirm your email subscription for CoderDojo Dallas',
        html='<a href="{0}">Click here to confirm your email subscription to CoderDojo Dallas.</a>'.format(url)
    )
    mail.send(msg)
