import json
from datetime import datetime, timezone
from typing import Callable
from dataclasses import dataclass, field
from jose import jws, jwe
from app.config import get_settings
from app.exceptions.exceptions import InvalidTokenError


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


class TokenProcessorAdapter:
    """ This adapts callable token serializers/deserializers
    to a standard interface. It's purpose is to allow the token
    generation and validation functions to be used with different
    processors without changes to their logic.

    The adapter makes the following assumptions about the processor:
     - It is a callable
     - It receives the token to be processed as a positional argument

    The attribute 'token_position_in_processor_args' determines the position
    where the token will be inserted in the arguments list which will be passed
    to the processor. The default is the first position.
    """

    def __init__(self, processor: Callable, args: list | None = None,
                 kwargs: dict | None = None):
        """

        :param processor: Processor callable
        :param args: Positional arguments to be passed to the processor
        :param kwargs: Keyword arguments to be passes to the processor
        """
        self.__processor = processor
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

        self.token_position_in_processor_args = 0

    def process(self, token: dict | str):
        """ Call the processor with the given arguments and token

        :param token: Token to be processed
        :return: Return value of the call to the processor
        """

        args = self.__args.copy()
        args.insert(self.token_position_in_processor_args, token)

        return self.__processor(*args, **self.__kwargs)


jws_serializer = TokenProcessorAdapter(
    jws.sign, args=[get_settings().jwt_signature_secret], kwargs={'algorithm': get_settings().jws_algo})

jwe_serializer = TokenProcessorAdapter(jwe.encrypt, args=[get_settings().jwt_encryption_secret], kwargs={
    'algorithm': get_settings().jwe_algo,
    'encryption': get_settings().jwe_encryption
})

jwe_decrypter = TokenProcessorAdapter(
    jwe.decrypt, args=[get_settings().jwt_encryption_secret])

jws_signature_verifier = TokenProcessorAdapter(
    jws.verify, args=[get_settings().jwt_signature_secret], kwargs={'algorithms': [get_settings().jws_algo]})


def parse_json_jwt(jwt: str | bytes) -> dict:
    try:
        jwt = json.loads(jwt)
        return jwt  # type: ignore
    except json.JSONDecodeError:
        raise InvalidTokenError


json_jwt_parser = TokenProcessorAdapter(parse_json_jwt)


def generate_signed_and_encrypted_jwt(token: dict) -> str:
    return jwe_serializer.process(
        jws_serializer.process(token)
    )


def decrypt_verify_and_parse_json_jwt(token: str) -> str:
    return json_jwt_parser.process(jws_signature_verifier.process(
        jwe_decrypter.process(token)
    ))


full_jwt_serializer = TokenProcessorAdapter(generate_signed_and_encrypted_jwt)
full_jwt_deserializer = TokenProcessorAdapter(
    decrypt_verify_and_parse_json_jwt)


def build_token_from_preset_and_serialize(preset: TokenPreset, serializer: TokenProcessorAdapter):
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

    return serializer.process(token)
