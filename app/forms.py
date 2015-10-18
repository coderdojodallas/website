from flask.ext.wtf import Form
from .models import User
from wtforms import StringField, BooleanField, validators


class MailingListForm(Form):
    first_name = StringField('first_name', [validators.InputRequired()])
    last_name = StringField('last_name', [validators.InputRequired()])
    email = StringField('email', [validators.InputRequired(), validators.Email()])
    age_group_1 = BooleanField('7-10', default=False)
    age_group_2 = BooleanField('11-14', default=False)
    age_group_3 = BooleanField('15-17', default=False)

    def age_group_is_chosen(self):
        return (
            self.age_group_1.data or
            self.age_group_2.data or
            self.age_group_3.data
        )

    def create_user(self):
        return User(
            first=self.first_name.data,
            last=self.last_name.data,
            email=self.email.data,
            age_group_1=self.age_group_1.data,
            age_group_2=self.age_group_2.data,
            age_group_3=self.age_group_3.data,
            confirmed=False
        )

    def fill_fields_with_user(self, user):
        self.first_name.data = user.first
        self.last_name.data = user.last
        self.email.data = user.email
        self.age_group_1.data = user.age_group_1
        self.age_group_2.data = user.age_group_2
        self.age_group_3.data = user.age_group_3
