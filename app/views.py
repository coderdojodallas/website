from app import app, db, mail, mailing_list_helper as mlh, messages
from enum import Enum
from flask import flash, redirect, render_template, url_for
from .forms import MailingListForm
from .models import User


class alert(Enum):
    info = 'alert-info'
    danger = 'alert-danger'
    success = 'alert-success'


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MailingListForm()

    if form.validate_on_submit():
        if not form.age_group_is_chosen():
            flash(messages.AGE_GROUP_VALIDATION, alert.danger)
        else:
            try:
                email = form.email.data
                user = User.query.filter_by(email=email).first()
                if user:
                    if user.confirmed:
                        flash(
                            messages.EMAIL_ADDRESS_SUBMITTED_AND_CONFIRMED.format(email),
                            alert.info
                        )
                    else:
                        flash(
                            messages.EMAIL_ADDRESS_SUBMITTED_NOT_CONFIRMED.format(email),
                            alert.info
                        )
                else:
                    user = form.create_user()
                    db.session.add(user)

                    _send_confirmation_email(user)

                    db.session.commit()
                    flash(
                        messages.CONFIRMATIONCONFIRMATION_EMAIL_SENT.format(email),
                        alert.success
                    )
            except Exception as e:
                db.session.rollback()
                raise e

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
    email = mlh.confirm_token(
        token,
        salt=app.config['EMAIL_CONFIRMATION_SALT'],
        expiration=app.config['EMAIL_CONFIRMATION_EXPIRATION']
    )
    if not email:
        flash(messages.CONFIRMATION_LINK_INVALID, alert.danger)
        return redirect(url_for('home'))

    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash(messages.CONFIRMATION_LINK_INVALID.format(email), alert.info)
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash(messages.CONFIRMATION_LINK_CONFIRMED.format(email), alert.success)
    return redirect(url_for('home'))


@app.route('/mailing_list_preferences/<token>', methods=['GET', 'POST'])
def mailing_list_preferences(token):
    email = mlh.confirm_token(
        token,
        salt=app.config['MAILING_LIST_PREFERENCES_SALT'],
    )
    if not email:
        flash(messages.MAILING_LIST_PREFERENCES_ERROR, alert.danger)
        return redirect(url_for('home'))

    user = User.query.filter_by(email=email).first_or_404()
    form = MailingListForm()

    # Don't fill fields on form submit
    if not form.validate_on_submit():
        form.fill_fields_with_user(user)
    else:
        # Edit user with form data, send email confirmation if necessary
        if not form.data_matches_user(user):
            form.update_user(user)
            if form.email.data != email:
                _send_confirmation_email(user)
                user.confirmed = False
                flash(
                    messages.CONFIRMATION_EMAIL_SENT.format(user.email),
                    alert.success
                )

            try:
                db.session.commit()
                flash(messages.MAILING_LIST_PREFERENCES_SUCCESS, alert.success)
            except Exception as e:
                db.session.rollback()
                raise e

    return render_template(
        'mailing_list_preferences.html',
        title='Mailing List Preferences',
        form=form,
        token=token
    )


@app.route('/unsubscribe/<token>', methods=['POST'])
def unsubscribe(token):
    email = mlh.confirm_token(
        token,
        salt=app.config['MAILING_LIST_PREFERENCES_SALT'],
    )
    if not email:
        flash(messages.MAILING_LIST_UNSUBSCRIBE_ERROR, alert.danger)
        return redirect(url_for('home'))

    user = User.query.filter_by(email=email).first_or_404()
    try:
        db.session.delete(user)
        db.session.commit()
        flash(messages.MAILING_LIST_UNSUBSCRIBE_SUCCESS, alert.success)
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        raise e


def _send_confirmation_email(user):
    token = mlh.generate_token(
        user.email,
        app.config['EMAIL_CONFIRMATION_SALT']
    )
    confirmation_url = url_for('confirm_email', token=token,
                               _external=True)
    mlh.send_confirmation_email(mail, user, confirmation_url)
