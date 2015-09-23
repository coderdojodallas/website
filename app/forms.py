from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, validators


class MailingListForm(Form):
    first_name = StringField('first_name', [validators.InputRequired()])
    last_name = StringField('last_name', [validators.InputRequired()])
    email = StringField('email', [validators.InputRequired()])
    age_group_1 = BooleanField('age_group_1', default=False)
    age_group_2 = BooleanField('age_group_2', default=False)
    age_group_3 = BooleanField('age_group_3', default=False)
