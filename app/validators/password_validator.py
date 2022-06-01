""" Implements the logic for
password validation, to ensure passwords
respect the following criteria:
- Length must be equal or larger than MINIMUM_PASSWORD_LENGTH
- Must have at least one uppercase character
- Must have at least one lowercase character
- Must have at least one numeric character
- Must have at least one special character
"""


MINIMUM_PASSWORD_LENGTH = 16


def respects_minimum_length(password: str):
    """Checks if the password respect the minimum
    length set in MINIMUM_PASSWORD_LENGTH

    :param password: Password string
    :type password: str

    :raises ValueError: ValueError is raised if
        the password does not respect the minimum length

    :return: Password string
    :rtype: str
    """

    if len(password) >= MINIMUM_PASSWORD_LENGTH:
        return password
    else:
        raise ValueError(
            f'Password must be at least {MINIMUM_PASSWORD_LENGTH} characters long.'
        )


def has_uppercase_character(password: str):
    """ Checks if the password has at least one
        uppercase character.

    :param password: Password string
    :type password: str

    :raises ValueError: Is raised if the password
        does not contain any uppercase characters.

    :return: Password string
    :rtype: str
    """

    chars = list(password)

    for char in chars:
        if char.isupper():
            return password

    raise ValueError(
        'Password must have at least one uppercase character.')


def has_lowercase_character(password: str):
    """ Checks if the password has at least one
    lowercase character.

    :param password: Password string
    :type password: str

    :raises ValueError: Is raised if the password
        does not contain any lowercase characters.

    :return: Password string
    :rtype: str
    """

    chars = list(password)

    for char in chars:
        if char.islower():
            return password

    raise ValueError(
        'Password must have at least one lowercase character.')


def has_numeric_characater(password: str):
    """ Checks if the password has at least one
        numeric character.

    :param password: Password string

    :raises ValueError: Raised if the password does
        not contain any numeric characters.

    :return: Password string
    """

    chars = list(password)

    for char in chars:
        if char.isnumeric():
            return password

    raise ValueError('Password must have at least one numeric character.')


def has_special_character(password: str):
    """ Checks if the password has at least one
        special character.

    :param password: Password string

    :raises ValueError: Raised if the password does not
        have any special characters

    :return: Password string
    """

    if any(not (char.isalnum() or char == ' ')
            for char in password):

        return password

    raise ValueError('Password does not have any special characaters.')


def validate(password: str):
    """ Runs the password through all the
     validators to check if it is valid

    :param password: Password string

    :raises ValueError: Raised when the
     password doesn't match any of the criteria
     for which the individual validators check.

    :return: Password string
    """

    validators = [
        respects_minimum_length,
        has_uppercase_character,
        has_lowercase_character,
        has_numeric_characater,
        has_special_character
    ]

    for validator in validators:
        try:
            password = validator(password)
        except ValueError as e:
            raise e

    return password
