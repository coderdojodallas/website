def age_group_validation():
    return 'You must select at least one age group.'


def email_address_already_submitted(email):
    return "The email address '{0}' has already been submitted.".format(email)


def confirmation_email_sent(email):
    return "Confirmation email sent to '{0}'.".format(email)


def confirmation_link_invalid():
    return 'The confirmation link is invalid or has expired. Please fill out the Mailing List form again.'


def confirmation_link_already_confirmed(email):
    return "The email address '{0}' has already been confirmed".format(email)


def confirmation_link_confirmed(email):
    return "The email address '{0}' has successfully been added to our mailing list. Thank you for your interest in CoderDojo Dallas!".format(email)


def mailing_list_preferences_confirmation_email(email):
    return "Confirmation email sent to '{0}'. You will not be able to update your preferences further until your email has been confirmed.".format(email)


def mailing_list_preferences_error():
    return 'The mailing list preferences for your email could not be loaded. Please contact help@coderdojodallas.com so we can assist in updating your mailing list preferences.'


def mailing_list_preferences_success():
    return 'Your preferences have been successfully updated.'


def mailing_list_unsubscribe_error():
    return 'There was an error unsubscribing your email address. Please contact help@coderdojodallas.com so we can assist you in unsubscribing.'


def mailing_list_unsubscribe_success():
    return 'You have been successfully unsubscribed from the mailing list.'
