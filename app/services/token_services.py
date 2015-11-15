from app import app
from itsdangerous import URLSafeTimedSerializer


def generate_token(string, salt):
    """ Generates and returns a token on the provided string and salt

    :param str string: the string to be tokenized
    :param str salt: the salt used for token generation
    :return: the token
    :rtype: str
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt):
    """ Confirms token and returns original, tokenized string.

    :param str token: the token
    :param str salt: the salt that was used for the token generation
    :return: the original, tokenized string or an empty string on error
    :rtype: str
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        string = serializer.loads(token, salt=salt)
    except:
        return ''
    return string
