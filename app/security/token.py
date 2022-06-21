from datetime import datetime, timezone
from typing import Callable

TOKEN_TEMPLATE = {
    'iat': -1,
    'exp': -1,
    'iss': 'bookmarks-api',
    'id': -1,
    'type': ''
}

REFRESH_TOKEN_EXPIRE_TIME_IN_SECONDS = 60 * 24 * 60
ACCESS_TOKEN_EXPIRE_TIME_IN_SECONDS = 30 * 60


class TokenSerializerAdapter:
    """ This adapts callable token serializers
    to a standard interface. It's purpose is to allow the token
    generation functions to be used with different  serializers
    without changes to their logic.

    The adapter makes the following assumptions about the serializer:
     - It is a callable
     - It receives the token to be serialized as a positional argument

    The attribute 'token_position_in_serializer_args' determines the position
    where the token will be inserted in the arguments list which will be passed
    to the serializer. The default is the first position.
    """

    def __init__(self, serializer: Callable, args: list | None = None,
                 kwargs: dict | None = None):
        """

        :param serializer: Serializer callable
        :param args: Positional arguments to be passed to the serializer
        :param kwargs: Keyword arguments to be passes to the serializer
        """
        self.__serializer = serializer
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

        self.token_position_in_serializer_args = 0

    def serialize(self, token: dict | str):
        """ Call the serializer with the given arguments and token

        :param token: Token to be serialized
        :return: Return value of the call to the serializer
        """

        args = self.__args
        args.insert(self.token_position_in_serializer_args, token)

        return self.__serializer(*args, **self.__kwargs)


def generate_refresh_token(id: int, serializer: TokenSerializerAdapter):
    """_summary_

    :param id: _description_
    :return: _description_
    """

    iat = datetime.now(timezone.utc).timestamp()

    token = TOKEN_TEMPLATE
    token['iat'] = iat
    token['exp'] = iat + REFRESH_TOKEN_EXPIRE_TIME_IN_SECONDS
    token['id'] = id
    token['type'] = 'refresh'

    return token


def generate_access_token(id: int, serializer: TokenSerializerAdapter):
    iat = datetime.now(timezone.utc).timestamp()

    token = TOKEN_TEMPLATE
    token['iat'] = iat
    token['exp'] = iat + ACCESS_TOKEN_EXPIRE_TIME_IN_SECONDS
    token['id'] = id
    token['type'] = 'access'

    return serializer.serialize(token)
