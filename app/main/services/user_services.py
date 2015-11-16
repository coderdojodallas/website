from app import db
from flask import current_app, url_for
from . import mailing_list_services as mls, token_services as ts
from ..models import User


def add_user(first_name, last_name, email, age_group_1, age_group_2, age_group_3):
    """ Adds user to mailing list and sends confirmation email

    :param str first_name: First name of user
    :param str last_name: Last name of user
    :param str email: Email address of user
    :param bool age_group_1: User has child in lower age group
    :param bool age_group_2: User has child in middle age group
    :param bool age_group_3: User has child in higher age group
    :return: the added user
    :rtype: app.models.User
    :raises DuplicateUserError: if user with provided email already exists
    """
    user = User.query.filter_by(email=email).first()
    if user:
        raise DuplicateUserError(email)

    user = User(
        first=first_name,
        last=last_name,
        email=email,
        age_group_1=age_group_1,
        age_group_2=age_group_2,
        age_group_3=age_group_3,
        confirmed=False
    )

    _create_token_and_send_confirmation_email(email)

    db.session.add(user)
    db.session.commit()
    return user


def confirm_user(user_token):
    """ Confirms user via user_token

    :param str user_token: the token for the user
    :return: the confirmed user
    :rtype: app.models.User
    :raises InvalidUserError: if user does not exist
    :raises AlreadyConfirmedUserError: if user has already been confirmed
    """
    email = ts.confirm_token(
        user_token,
        salt=current_app.config['MAILING_LIST_USER_SALT']
    )
    user = User.query.filter_by(email=email).first()

    if not user:
        raise InvalidUserError(email)
    if user.confirmed:
        raise AlreadyConfirmedUserError(email)

    user.confirmed = True
    db.session.commit()
    return user


def edit_user(user_token, first_name, last_name, email, age_group_1,
              age_group_2, age_group_3):
    """ Edits user info, sends confirmation email if email has changed

    :param str user_token: The token for the user
    :param str first_name: First name of user
    :param str last_name: Last name of user
    :param str email: Email address of user
    :param bool age_group_1: User has child in lower age group
    :param bool age_group_2: User has child in middle age group
    :param bool age_group_3: User has child in higher age group
    :return: the edited user
    :rtype: app.models.User
    :raises InvalidUserError: if user does not exist
    :raises NotConfirmedUserError: if user has not been confirmed
    """
    original_email = ts.confirm_token(
        user_token,
        current_app.config['MAILING_LIST_USER_SALT']
    )
    user = User.query.filter_by(email=original_email).first()
    if not user:
        raise InvalidUserError(original_email)
    if not user.confirmed:
        raise NotConfirmedUserError(original_email)

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.age_group_1 = age_group_1
    user.age_group_2 = age_group_2
    user.age_group_3 = age_group_3

    if original_email != email:
        _create_token_and_send_confirmation_email(email)
        user.confirmed = False

    db.session.commit()
    return user


def delete_user(user_token):
    """ Deletes user

    :param str user_token: the token for the user
    """
    email = ts.confirm_token(
        user_token,
        salt=current_app.config['MAILING_LIST_USER_SALT'],
    )
    user = User.query.filter_by(email=email).first()
    if not user:
        raise InvalidUserError(email)
    db.session.delete(user)
    db.session.commit()


def get_user(user_token):
    """ Gets user object

    :param str user_token: the token for the user
    :return: the User for the provided user_token
    :rtype: app.models.User
    :raises InvalidUserError: if user with provided email does not exist
    """
    email = ts.confirm_token(
        user_token,
        salt=current_app.config['MAILING_LIST_USER_SALT'],
    )
    user = User.query.filter_by(email=email).first()
    if not user:
        raise InvalidUserError(email)

    return user


def _create_token_and_send_confirmation_email(email):
    token = ts.generate_token(email, current_app.config['MAILING_LIST_USER_SALT'])
    url = url_for('main.confirm_email', token=token, _external=True)
    mls.send_confirmation_email(email, url)


class UserError(Exception):
    def __init__(self, email):
        self.email = email


class AlreadyConfirmedUserError(UserError):
    def __str__(self):
        return "The user with email address '{0}' has already been confirmed.".format(self.email)


class DuplicateUserError(UserError):
    def __str__(self):
        return "The user with email address '{0}' already exists.".format(self.email)


class InvalidUserError(UserError):
    def __str__(self):
        return "The user with email address '{0}' does not exist.".format(self.email)


class NotConfirmedUserError(UserError):
    def __str__(self):
        return "The user with email address '{0}' has not yet been confirmed.".format(self.email)
