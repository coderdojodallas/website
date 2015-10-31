from app import messages
from flask import flash
from flask.ext.wtf import Form
from .models import User
from wtforms import StringField, BooleanField, validators


class MailingListForm(Form):
    """ Form that handles the maling list """
    first_name = StringField('first_name', [validators.InputRequired()])
    last_name = StringField('last_name', [validators.InputRequired()])
    email = StringField('email', [validators.InputRequired(), validators.Email()])
    age_group_1 = BooleanField('7-10', default=False)
    age_group_2 = BooleanField('11-14', default=False)
    age_group_3 = BooleanField('15-17', default=False)

    def validate(self):
        """ Overriden to assure at least one age group is chosen. """
        if not Form.validate(self):
            return False

        age_group_chosen = self._age_group_is_chosen()
        if not age_group_chosen:
            flash(messages.age_group_validation(), 'alert-danger')

        return age_group_chosen

    def create_user(self):
        """ Creates models.User object from form data.

        :return: User
        """
        return User(
            first=self.first_name.data,
            last=self.last_name.data,
            email=self.email.data,
            age_group_1=self.age_group_1.data,
            age_group_2=self.age_group_2.data,
            age_group_3=self.age_group_3.data,
            confirmed=False
        )

    def update_user(self, user):
        """ Updates user with updated form data. Does not edit user.confirmed.

        :param user: The user to be updates
        :type user: User
        """
        user.first = self.first_name.data
        user.last = self.last_name.data
        user.email = self.email.data
        user.age_group_1 = self.age_group_1.data
        user.age_group_2 = self.age_group_2.data
        user.age_group_3 = self.age_group_3.data

    def fill_fields_with_user(self, user):
        """ Fills form fields with data from provided user.

        :param user: The user used to fill the form
        :type user: User
        """
        self.first_name.data = user.first
        self.last_name.data = user.last
        self.email.data = user.email
        self.age_group_1.data = user.age_group_1
        self.age_group_2.data = user.age_group_2
        self.age_group_3.data = user.age_group_3

    def data_matches_user(self, user):
        """ Returns true if form data matches provided user.

        :param user: The user that will be matched against the form data
        :type user: User

        :return: bool
        """
        print(self.first_name.data)
        return (
            self.first_name.data == user.first and
            self.last_name.data == user.last and
            self.email.data == user.email and
            self.age_group_1.data == user.age_group_1 and
            self.age_group_2.data == user.age_group_2 and
            self.age_group_3.data == user.age_group_3
        )

    def _age_group_is_chosen(self):
        """ Returns true if at least one age group is chosen.

        :return: bool
        """
        return (
            self.age_group_1.data or
            self.age_group_2.data or
            self.age_group_3.data
        )
