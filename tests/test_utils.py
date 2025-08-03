from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import get_exchange_rate
from src.utils import get_transaction_amount, load_transactions


@pytest.fixture
def sample_transactions():
    return {
        "rub_transaction": {"amount": "100.0", "currency": "RUB"},
        "usd_transaction": {"amount": "10.0", "currency": "USD"},
        "eur_transaction": {"amount": "5.0", "currency": "EUR"},
    }


def test_rub_transaction(sample_transactions):
    assert get_transaction_amount(sample_transactions["rub_transaction"]) == 100.0


@patch('src.external_api.get_exchange_rate')
def test_usd_transaction(mock_get_rate, sample_transactions):
    mock_get_rate.return_value = 75.0
    assert get_transaction_amount(sample_transactions["usd_transaction"]) == 750.0
    mock_get_rate.assert_called_once_with("USD")


@patch('src.external_api.get_exchange_rate')
def test_eur_transaction(mock_get_rate, sample_transactions):
    mock_get_rate.return_value = 85.0
    assert get_transaction_amount(sample_transactions["eur_transaction"]) == 425.0


def test_invalid_currency():
    with pytest.raises(ValueError):
        get_transaction_amount({"amount": "100", "currency": "GBP"})


@patch('src.external_api.requests.get')
def test_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("API error")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        get_exchange_rate("USD")


class TestLoadTransactionsTryExcept:
    """Тесты для блока try-except в функции load_transactions"""

    def test_file_not_found(self, tmp_path, caplog):
        """Тест обработки отсутствующего файла"""
        file_path = tmp_path / "nonexistent.json"

        result = load_transactions(file_path)

        assert result == []
        assert "WARNING" in caplog.text and "Файл не найден" in caplog.text

    def test_json_decode_error(self, tmp_path, caplog):
        """Тест обработки невалидного JSON"""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("{invalid json}", encoding='utf-8')

        result = load_transactions(file_path)

        assert result == []
        assert "ERROR" in caplog.text and "Ошибка декодирования JSON" in caplog.text

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_file_permission_error(self, mock_open, tmp_path, caplog):
        """Тест обработки ошибки доступа к файлу"""
        file_path = tmp_path / "no_access.json"
        file_path.touch()

        result = load_transactions(file_path)

        assert result == []
        assert "ERROR" in caplog.text and "Непредвиденная ошибка" in caplog.text
        assert "Permission denied" in caplog.text

    @patch('json.load', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid byte"))
    def test_unicode_decode_error(self, mock_json, tmp_path, caplog):
        """Тест обработки ошибки декодирования Unicode"""
        file_path = tmp_path / "unicode_error.json"
        file_path.touch()

        result = load_transactions(file_path)

        assert result == []
        assert "ERROR" in caplog.text and "Непредвиденная ошибка" in caplog.text
        assert "invalid byte" in caplog.text

    @patch('pathlib.Path.exists', side_effect=Exception("Unexpected exists error"))
    def test_unexpected_error_in_exists_check(self, mock_exists, caplog):
        """Тест обработки непредвиденной ошибки при проверке существования файла"""
        result = load_transactions("any_path.json")

        assert result == []
        assert "ERROR" in caplog.text and "Непредвиденная ошибка" in caplog.text
        assert "Unexpected exists error" in caplog.text

    def test_empty_file(self, tmp_path, caplog):
        """Тест обработки пустого файла"""
        file_path = tmp_path / "empty.json"
        file_path.touch()

        result = load_transactions(file_path)

        assert result == []
        assert "ERROR" in caplog.text and "Ошибка декодирования JSON" in caplog.text
