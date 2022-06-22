from datetime import datetime, timezone
from typing import Callable
from dataclasses import dataclass, field


@dataclass
class TokenPreset:
    """ Holds parameters to configure the generation of
    a token

    """

    token_type: str
    time_to_expire_in_seconds: int

    uid: int | None = field(default=None)


refresh_token_preset = TokenPreset(
    token_type='refresh', time_to_expire_in_seconds=60 * 60 * 24)
access_token_preset = TokenPreset(
    token_type='access', time_to_expire_in_seconds=30 * 60)


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


def build_token_from_preset_and_serialize(preset: TokenPreset, serializer: TokenSerializerAdapter):
    """ Builds a token from a preset and the serializes it with the
    given serializer, returning the result.

    :param preset: TokenPreset object containing parameters to generate the token
    :param serializer: TokenSerializerAdapter object, containing the serializer callable
    and arguments to be used to serialize the token.

    :return: Serialized token
    """

    iat = datetime.now(timezone.utc).timestamp()

    token = {
        'iat': -1,
        'exp': -1,
        'iss': 'bookmarks-api',
        'uid': -1,
        'type': ''
    }

    token['iat'] = iat
    token['exp'] = iat + preset.time_to_expire_in_seconds
    token['uid'] = preset.uid
    token['type'] = preset.token_type

    return serializer.serialize(token)
