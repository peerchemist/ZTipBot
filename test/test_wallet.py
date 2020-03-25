from unittest.mock import patch

from src.wallet import check_balance


MOCK_USER_ID = 12345


@patch('src.wallet.get_balance')
def test_negative_balance(mock_get_balance):
    mock_get_balance.return_value = -1.0
    assert not check_balance(MOCK_USER_ID, -1.1)
    assert not check_balance(MOCK_USER_ID, -1.0)
    assert not check_balance(MOCK_USER_ID, 0.0)
    assert not check_balance(MOCK_USER_ID, 1.0)


@patch('src.wallet.get_balance')
def test_zero_balance(mock_get_balance):
    mock_get_balance.return_value = 0.0
    assert check_balance(MOCK_USER_ID, -1.0)
    assert check_balance(MOCK_USER_ID, 0.0)
    assert not check_balance(MOCK_USER_ID, 0.1)
    assert not check_balance(MOCK_USER_ID, 1.0)


@patch('src.wallet.get_balance')
def test_positive_balance(mock_get_balance):
    mock_get_balance.return_value = 1.0
    assert check_balance(MOCK_USER_ID, -1.0)
    assert check_balance(MOCK_USER_ID, 0.0)
    assert check_balance(MOCK_USER_ID, 1.0)
    assert not check_balance(MOCK_USER_ID, 1.1)
