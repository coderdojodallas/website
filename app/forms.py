from flask.ext.wtf import Form
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
