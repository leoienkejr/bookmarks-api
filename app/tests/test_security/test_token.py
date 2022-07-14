from datetime import datetime, timezone
import pytest
from ...security.token import (build_token_from_preset_and_serialize as build_token,
                               access_token_preset,
                               TokenProcessorAdapter,
                               parse_json_jwt)

from app.exceptions.exceptions import InvalidTokenError


def fake_processor(token):
    token['passed_fake_processor'] = True
    return token


@pytest.mark.asyncio
async def test_TokenProcessorAdapter():

    adapted_fake_processor = TokenProcessorAdapter(
        fake_processor, args=['foo'], kwargs={'bar': True})

    assert adapted_fake_processor.processor is fake_processor  # type: ignore
    # type: ignore
    assert adapted_fake_processor.args[0] == 'foo'
    assert adapted_fake_processor.kwargs.get(     # type: ignore
        'bar') is True


@pytest.mark.asyncio
async def test_TokenProcessorAdapter_serialize():
    token = {'foo': 'bar'}
    adapted_fake_processor = TokenProcessorAdapter(fake_processor)
    serialized_token = adapted_fake_processor.process(token)

    assert serialized_token.get('foo') == 'bar'
    assert serialized_token.get('passed_fake_processor') is True


@pytest.mark.asyncio
async def test_build_token_from_preset_and_serialize():

    adapted_fake_processor = TokenProcessorAdapter(fake_processor)
    preset = access_token_preset
    preset.uid = 5597

    before_iat = datetime.now(timezone.utc).timestamp()
    token = build_token(access_token_preset, adapted_fake_processor)
    after_iat = datetime.now(timezone.utc).timestamp()

    assert token.get('passed_fake_processor') is True
    assert token['iat'] >= before_iat and token['iat'] <= after_iat
    assert token['exp'] == (
        token['iat'] + preset.time_to_expire_in_seconds)
    assert token['uid'] == preset.uid
    assert token['type'] == preset.token_type


@pytest.mark.asyncio
async def test_parse_json_jwt():
    nice_json_token = '{"foo": "bar"}'
    bad_token = "faoofjwopekdfjan"

    assert isinstance(parse_json_jwt(nice_json_token), dict)

    try:
        parse_json_jwt(bad_token)
    except Exception as e:
        assert e == InvalidTokenError
