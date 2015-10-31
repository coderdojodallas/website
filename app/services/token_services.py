from app import app
from itsdangerous import URLSafeTimedSerializer


class InvalidTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self, token):
        return 'The token {0} could not be confirmed'.format(token)


def generate_token(email, salt):
    """ Generates and returns a token based on the email address and salt.

    :param email: the email address used for token generation
    :type email: str
    :param salt: the salt used for token generation
    :type salt: str

    :return: str
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=None):
    """ Confirms token. Returns email address on success, or an empty string on failure.

    :param token: the token to be confirmed
    :type token: str
    :param salt: the salt that was used for the token generation
    :type salt: str
    :param expiration: the expiration of the token in seconds
    :type expiration: int

    :return: str
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except:
        return ''
    return email
