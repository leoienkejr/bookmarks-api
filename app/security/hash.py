'''
Functions for hashing and verification of passwords
'''

import bcrypt

BCRYPT_ROUNDS = 16


def hash_password(password: str) -> str:
    """ Hash a given password

    :param password: Password to be hashed
    :return: Hashed password
    """

    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
    return str(hashed_password, 'utf-8')


def verify_password(password: str, hash: str) -> bool:
    '''
    Verify if a password matches a hash
    '''

    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hash, 'utf-8'))
