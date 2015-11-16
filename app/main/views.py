from flask import flash, redirect, render_template, url_for
from . import main, messages as msg
from .forms import MailingListForm
from .services import user_services as us


@main.route('/', methods=['GET', 'POST'])
def home():
    form = MailingListForm()
    if form.validate_on_submit():
        try:
            us.add_user(
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.age_group_1.data,
                form.age_group_2.data,
                form.age_group_3.data
            )
            flash(msg.confirmation_email_sent(form.email.data), 'alert-success')
        except us.DuplicateUserError as e:
            flash(msg.email_address_already_submitted(e.email))
    return render_template('home.html', title='Home', form=form)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@main.route('/register')
def register():
    return render_template('register.html', title='Register')


@main.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        user = us.confirm_user(token)
        flash(msg.confirmation_link_confirmed(user.email), 'alert-success')
    except us.InvalidUserError:
        flash(msg.confirmation_link_invalid(), 'alert-danger')
    except us.AlreadyConfirmedUserError as e:
        flash(msg.confirmation_link_already_confirmed(e.email), 'alert-info')

    return redirect(url_for('main.home'))


@main.route('/mailing_list_preferences/<token>', methods=['GET', 'POST'])
def mailing_list_preferences(token):
    form = MailingListForm()

    try:
        # Fill form with user data if not submitting form
        if not form.validate_on_submit():
            user = us.get_user(token)
            if not user.confirmed:
                flash(msg.mailing_list_preferences_not_confirmed_error(),
                      'alert-danger')
                return redirect(url_for('main.home'))
            form.fill_fields_with_user(user)
        else:
            user = us.edit_user(
                token,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.age_group_1.data,
                form.age_group_2.data,
                form.age_group_3.data
            )
            if not user.confirmed:
                flash(msg.mailing_list_preferences_confirmation_email(user.email),
                      'alert-info')
            flash(msg.mailing_list_preferences_success(), 'alert-success')

    except us.InvalidUserError:
        flash(msg.mailing_list_preferences_error(), 'alert-danger')
        return redirect(url_for('main.home'))
    except us.NotConfirmedUserError as e:
        flash(msg.mailing_list_preferences_not_confirmed_error(), 'alert-danger')

    return render_template(
        'mailing_list_preferences.html',
        title='Mailing List Preferences',
        form=form,
        token=token
    )


@main.route('/unsubscribe/<token>', methods=['POST'])
def unsubscribe(token):
    try:
        us.delete_user(token)
        flash(msg.mailing_list_unsubscribe_success(), 'alert-success')
    except us.InvalidUserError:
        flash(msg.mailing_list_unsubscribe_error(), 'alert-danger')
    return redirect(url_for('main.home'))
