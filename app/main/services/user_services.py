from app import db
from flask import current_app, url_for
from ..models import User
from ..signals import email_address_changed


def add_user(first_name, last_name, email, age_group_1, age_group_2, age_group_3):
    """ Adds user to mailing list, sends 'email_address_changed' signal

    :param str first_name: first name of user
    :param str last_name: last name of user
    :param str email: email address of user
    :param bool age_group_1: user has child in lower age group
    :param bool age_group_2: user has child in middle age group
    :param bool age_group_3: user has child in higher age group
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

    db.session.add(user)
    db.session.commit()

    # Every add is an email address change, send signal
    email_address_changed.send(add_user, email=user.email)

    return user


def confirm_user(email):
    """ Confirms user

    :param str email: the email for the user
    :return: the confirmed user
    :rtype: app.models.User
    :raises InvalidUserError: if user does not exist
    :raises AlreadyConfirmedUserError: if user has already been confirmed
    """
    user = User.query.filter_by(email=email).first()

    if not user:
        raise InvalidUserError(email)
    if user.confirmed:
        raise AlreadyConfirmedUserError(email)

    user.confirmed = True
    db.session.commit()
    return user


def edit_user(current_email, first_name, last_name, email, age_group_1,
              age_group_2, age_group_3):
    """ Edits user info, sends 'email_address_changed' signal

    :param str current_email: current email address for the user
    :param str first_name: first name of user
    :param str last_name: last name of user
    :param str email: email address of user
    :param bool age_group_1: user has child in lower age group
    :param bool age_group_2: user has child in middle age group
    :param bool age_group_3: user has child in higher age group
    :return: the edited user
    :rtype: app.models.User
    :raises InvalidUserError: if user does not exist
    :raises NotConfirmedUserError: if user has not been confirmed
    """
    user = User.query.filter_by(email=current_email).first()
    if not user:
        raise InvalidUserError(current_email)
    if not user.confirmed:
        raise NotConfirmedUserError(current_email)

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.age_group_1 = age_group_1
    user.age_group_2 = age_group_2
    user.age_group_3 = age_group_3

    if current_email != email:
        user.confirmed = False

    db.session.commit()

    # Send signal if email address changed (affter db commit, just in case)
    if not user.confirmed:
        email_address_changed.send(edit_user, email=user.email)

    return user


def delete_user(email):
    """ Deletes user

    :param str email: email address for the user
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        raise InvalidUserError(email)
    db.session.delete(user)
    db.session.commit()


def get_user(email):
    """ Gets user object

    :param str email: email address for the user
    :return: the User for the provided email address
    :rtype: app.models.User
    :raises InvalidUserError: if user does not exist
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        raise InvalidUserError(email)
    return user


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
