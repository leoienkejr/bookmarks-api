import pytest
from ...validators import password_validator


def test_respects_minimum_length():
    """ Tests password_validator.respects_minimum_length()
    """

    password_validator.MINIMUM_PASSWORD_LENGTH = 16
    pwd = 'a' * password_validator.MINIMUM_PASSWORD_LENGTH
    invalid_pwd = 'a' * (password_validator.MINIMUM_PASSWORD_LENGTH - 1)

    assert password_validator.respects_minimum_length(pwd) == pwd

    with pytest.raises(ValueError):
        password_validator.respects_minimum_length(invalid_pwd)


def test_has_lowercase_characater():
    """ Tests password_validator.has_lowercase_characater()
    """

    pwd = 'aa'
    invalid_pwd = 'AA'

    assert password_validator.has_lowercase_character(pwd) == pwd

    with pytest.raises(ValueError):
        password_validator.has_lowercase_character(invalid_pwd)


def test_has_uppercase_characater():
    """ Tests password_validator.has_uppercase_characater()
    """

    pwd = 'AA'
    invalid_pwd = 'aa'

    assert password_validator.has_uppercase_character(pwd) == pwd

    with pytest.raises(ValueError):
        password_validator.has_uppercase_character(invalid_pwd)


def test_has_numeric_character():
    """ Tests password_validator.has_numeric_character()
    """

    pwd = '1'
    invalid_pwd = 'a'

    assert password_validator.has_numeric_characater(pwd) == pwd

    with pytest.raises(ValueError):
        password_validator.has_numeric_characater(invalid_pwd)


def test_has_special_character():
    """ Tests password_validator.has_special_character()
    """

    pwd = '@'
    invalid_pwd = 'a'

    assert password_validator.has_special_character(pwd) == pwd

    with pytest.raises(ValueError):
        password_validator.has_special_character(invalid_pwd)
