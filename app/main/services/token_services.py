from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def generate_token(data, salt):
    """ Generates and returns a token on the provided data and salt

    :param str data: the data to be tokenized
    :param str salt: the salt used for token generation
    :return: the token
    :rtype: str
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(data, salt=salt)


def confirm_token(token, salt):
    """ Confirms token and returns original, tokenized data.

    :param str token: the token
    :param str salt: the salt that was used for the token generation
    :return: the original, tokenized data or an empty data on error
    :rtype: str
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, salt=salt)
    except:
        return ''
    return data
