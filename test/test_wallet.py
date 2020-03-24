from unittest.mock import patch

from src.wallet import check_balance


MOCK_USER_ID = 12345


class TestGetBalance:

    @patch('src.wallet.get_balance')
    def test_negative_balance(self, mock_get_balance):
        mock_get_balance.return_value = -1.0
        assert check_balance(MOCK_USER_ID, -1.1) == False
        assert check_balance(MOCK_USER_ID, -1.0) == False
        assert check_balance(MOCK_USER_ID, 0.0) == False
        assert check_balance(MOCK_USER_ID, 1.0) == False

    @patch('src.wallet.get_balance')
    def test_zero_balance(self, mock_get_balance):
        mock_get_balance.return_value = 0.0
        assert check_balance(MOCK_USER_ID, -1.0) == True
        assert check_balance(MOCK_USER_ID, 0.0) == True
        assert check_balance(MOCK_USER_ID, 0.1) == False
        assert check_balance(MOCK_USER_ID, 1.0) == False

    @patch('src.wallet.get_balance')
    def test_positive_balance(self, mock_get_balance):
        mock_get_balance.return_value = 1.0
        assert check_balance(MOCK_USER_ID, -1.0) == True
        assert check_balance(MOCK_USER_ID, 0.0) == True
        assert check_balance(MOCK_USER_ID, 1.0) == True
        assert check_balance(MOCK_USER_ID, 1.1) == False
