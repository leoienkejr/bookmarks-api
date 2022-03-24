from ..config import Settings, get_settings


def test_get_settings_return_type():
    result = get_settings()
    assert isinstance(result, Settings)
