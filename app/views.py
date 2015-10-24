from app import app, db, mail, mailing_list_helper as mlh
from flask import flash, redirect, render_template, url_for
from .forms import MailingListForm
from .models import User


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MailingListForm()

    if form.validate_on_submit():
        if not form.age_group_is_chosen():
            flash('You must select at least one age group.', 'alert-danger')
        else:
            try:
                user = User.query.filter_by(email=form.email.data).first()
                if user:
                    confirm_text = _get_confirm_text(user)
                    flash("The email address '{0}' has already been "
                          "submitted{1}".format(user.email, confirm_text), 'alert-info')
                else:
                    user = form.create_user()
                    db.session.add(user)

                    _send_confirmation_email(user)

                    db.session.commit()
                    flash('Confirmation email sent to {0}.'.format(form.email.data),
                          'alert-success')
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
        flash('The confimation link is invalid or has expired. '
              'Please fill out the Mailing List form again.', 'alert-danger')
        return redirect(url_for('home'))

    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash("The email address '{0}' has already been "
              "confirmed.".format(email), 'alert-info')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("The email address '{0}' has successfully been added to "
              "our mailing list. Thank you for your interest in "
              "CoderDojo Dallas!".format(email), 'alert-success')
    return redirect(url_for('home'))


@app.route('/mailing_list_preferences/<token>', methods=['GET', 'POST'])
def mailing_list_preferences(token):
    email = ''
    try:
        email = mlh.confirm_token(
            token,
            salt=app.config['EMAIL_PREFERENCES_SALT'],
        )
    except:
        flash('The mailing list preferences for your email could not be loaded. '
              'Please contact help@coderdojodallas.com so we can assist in '
              'updating your mailing list preferences.')
        return redirect(url_for('home'))

    user = User.query.filter_by(email=email).first_or_404()
    form = MailingListForm()
    form.fill_fields_with_user(user)
    return render_template('mailing_list_preferences.html', title='Mailing List Preferences')


@app.route('/mailing_list_preferences/test', methods=['GET', 'POST'])
def mailing_list_preferences_test():
    """
    NOTE: This method exists only for easy testing and development of the
    mailing list preferences feature. This should be moved into the
    'mailing_list_preferences' method when the feature is more complete.

    TODO: Unsubscribe logic
    """
    email = 'austincrft@gmail.com'
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
                flash('Confirmation email sent to {0}.'.format(user.email),
                      'alert-success')

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    return render_template(
        'mailing_list_preferences.html',
        title='Mailing List Preferences',
        form=form
    )


def _get_confirm_text(user):
    if user.confirmed:
        return (' and confirmed. You will receive '
                'future CoderDojo Dallas emails.')
    else:
        return (', but not confirmed. Check your inbox '
                'for an email with confirmation steps.')


def _send_confirmation_email(user):
    token = mlh.generate_token(
        user.email,
        app.config['EMAIL_CONFIRMATION_SALT']
    )
    confirmation_url = url_for('confirm_email', token=token,
                               _external=True)
    mlh.send_confirmation_email(mail, user, confirmation_url)
