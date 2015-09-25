from flask import flash
from app import app


def flash_errors(form, excluded_fieldnames=[]):
    for field, errors in form.errors.items():
        if field in excluded_fieldnames:
            return
        for error in errors:
            message = '{0}'.format(error)
            if app.debug:
                print(message)
            flash(message)
