import pytest
from unittest.mock import Mock, patch
from ...crud import user

pytest_plugins = ('pytest_asyncio')


class MockDBSession(Mock):
    def __init__(self):
        super().__init__()
        self._flush_calls = 0

    async def flush(self, *args):
        self._flush_calls += 1
        return None

    def add(self, *args):
        args[0].id = 1
        return args[0]


def fake_hash_password(password: str) -> str:
    return password + '@@@'


@pytest.mark.asyncio
@patch('app.crud.user.User')
async def test_create_user(mock_user_obj):
    '''
    Test the succesful creation of users with the create_user function
    '''

    db = MockDBSession()
    email = 'a@email.com'
    password = '123'

    result = await user.create_user(db=db, email=email, password=password, hash_func=fake_hash_password)

    mock_user_obj.assert_called_with(
        email=email, hashed_password=fake_hash_password(password))
    assert db._flush_calls == 1
    assert result.id == 1
