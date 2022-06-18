TOKEN_TEMPLATE = {
    'iat': -1,
    'exp': -1,
    'iss': 'bookmarks-api',
    'id': -1,
    'type': ''
}


def generate_refresh_token(id: int):
    token = TOKEN_TEMPLATE
    token['id'] = id

    return token


def generate_access_token(id: int):
    token = TOKEN_TEMPLATE
    token['id'] = id

    return token
