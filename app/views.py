from app import app, db, mail
from flask import redirect, render_template, url_for
from .forms import MailingListForm
from .models import User
from .services import mailing_list_services as mls
from .services.token_services import InvalidTokenError


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MailingListForm()
    if form.validate_on_submit():
        mls.add_user(form)
    return render_template('home.html', title='Home', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        mls.confirm_user(token)
    except InvalidTokenError:
        pass
    return redirect(url_for('home'))


@app.route('/mailing_list_preferences/<token>', methods=['GET', 'POST'])
def mailing_list_preferences(token):
    form = MailingListForm()
    try:
        mls.edit_user(token, form)
    except InvalidTokenError:
        return redirect(url_for('home'))
    return render_template(
        'mailing_list_preferences.html',
        title='Mailing List Preferences',
        form=form,
        token=token
    )


@app.route('/unsubscribe/<token>', methods=['POST'])
def unsubscribe(token):
    try:
        mls.delete_user(token)
    except (InvalidTokenError, mls.InvalidUserError):
        pass
    return redirect(url_for('home'))
