import pytest
from datetime import datetime, timezone
from ...security.token import (build_token_from_preset_and_serialize as build_token,
                               access_token_preset, TokenSerializerAdapter)


def fake_serializer(token):
    token['passed_fake_serializer'] = True
    return token


@pytest.mark.asyncio
async def test_TokenSerializerAdapter():

    adapted_fake_serializer = TokenSerializerAdapter(
        fake_serializer, args=['foo'], kwargs={'bar': True})

    assert adapted_fake_serializer._TokenSerializerAdapter__serializer is fake_serializer  # type: ignore
    assert adapted_fake_serializer._TokenSerializerAdapter__args[0] == 'foo'    # type: ignore
    assert adapted_fake_serializer._TokenSerializerAdapter__kwargs.get(     # type: ignore
        'bar') is True


@pytest.mark.asyncio
async def test_TokenSerializerAdapter_serialize():
    token = {'foo': 'bar'}
    adapted_fake_serializer = TokenSerializerAdapter(fake_serializer)
    serialized_token = adapted_fake_serializer.serialize(token)

    assert serialized_token.get('foo') == 'bar'
    assert serialized_token.get('passed_fake_serializer') is True


@pytest.mark.asyncio
async def test_build_token_from_preset_and_serialize():

    adapted_fake_serializer = TokenSerializerAdapter(fake_serializer)
    preset = access_token_preset
    preset.uid = 5597

    before_iat = datetime.now(timezone.utc).timestamp()
    token = build_token(access_token_preset, adapted_fake_serializer)
    after_iat = datetime.now(timezone.utc).timestamp()

    assert token.get('passed_fake_serializer') is True
    assert token['iat'] >= before_iat and token['iat'] <= after_iat
    assert token['exp'] == (
        token['iat'] + preset.time_to_expire_in_seconds)
    assert token['uid'] == preset.uid
    assert token['type'] == preset.token_type
