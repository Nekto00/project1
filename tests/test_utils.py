from unittest.mock import MagicMock, patch

import pytest
import requests
import re

from src.external_api import get_exchange_rate
from src.utils import get_transaction_amount, load_transactions, process_bank_search, process_bank_operations
from collections import defaultdict

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

def test_empty_search_returns_all_data():
    """Если строка поиска пустая, возвращается копия исходных данных."""
    data = [
        {"description": "Payment for groceries", "amount": 50},
        {"description": "Salary", "amount": 1000},
    ]
    result = process_bank_search(data, "")
    assert result == data  # Проверяем, что вернулась копия данных
    assert result is not data  # Убедимся, что это именно копия, а не исходный список

def test_case_insensitive_search():
    """Поиск должен быть регистронезависимым."""
    data = [
        {"description": "Payment for Groceries", "amount": 50},
        {"description": "salary deposit", "amount": 1000},
    ]
    result = process_bank_search(data, "groceries")
    assert len(result) == 1
    assert result[0]["description"] == "Payment for Groceries"

def test_partial_match():
    """Поиск должен находить частичные совпадения."""
    data = [
        {"description": "Netflix Subscription", "amount": 15},
        {"description": "Spotify Premium", "amount": 10},
    ]
    result = process_bank_search(data, "net")
    assert len(result) == 1
    assert "Netflix" in result[0]["description"]

def test_no_matches_returns_empty_list():
    """Если совпадений нет, возвращается пустой список."""
    data = [
        {"description": "Uber Ride", "amount": 20},
    ]
    result = process_bank_search(data, "Taxi")
    assert result == []

def test_missing_description_field():
    """Если у элемента нет поля 'description', он игнорируется."""
    data = [
        {"description": "Coffee", "amount": 5},
        {"amount": 100},  # Нет описания
        {"description": "Books", "amount": 30},
    ]
    result = process_bank_search(data, "coffee")
    assert len(result) == 1
    assert result[0]["description"] == "Coffee"

def test_special_characters_in_search():
    """Поиск должен корректно обрабатывать спецсимволы."""
    data = [
        {"description": "Payment (VIP)", "amount": 500},
    ]
    result = process_bank_search(data, "(VIP)")
    assert len(result) == 1

def test_basic_category_counting():
    """Проверяет базовый подсчёт операций по категориям."""
    data = [
        {"description": "Coffee at Starbucks", "amount": 5},
        {"description": "Groceries from Walmart", "amount": 50},
        {"description": "Uber ride to work", "amount": 15},
        {"description": "Starbucks coffee again", "amount": 6},
    ]
    categories = ["coffee", "groceries", "uber"]
    result = process_bank_operations(data, categories)
    assert result == {"coffee": 2, "groceries": 1, "uber": 1}

def test_case_insensitivity():
    """Проверяет регистронезависимость поиска категорий."""
    data = [
        {"description": "COFFEE at Starbucks", "amount": 5},
        {"description": "groceries from Whole Foods", "amount": 70},
    ]
    categories = ["Coffee", "Groceries"]
    result = process_bank_operations(data, categories)
    assert result == {"Coffee": 1, "Groceries": 1}

def test_missing_categories():
    """Проверяет обработку категорий, которых нет в данных."""
    data = [
        {"description": "Netflix subscription", "amount": 15},
    ]
    categories = ["food", "transport"]
    result = process_bank_operations(data, categories)
    assert result == {"food": 0, "transport": 0}

def test_empty_data():
    """Проверяет работу с пустым списком операций."""
    data = []
    categories = ["coffee", "food"]
    result = process_bank_operations(data, categories)
    assert result == {"coffee": 0, "food": 0}

def test_operations_without_description():
    """Проверяет игнорирование операций без поля 'description'."""
    data = [
        {"description": "Restaurant bill", "amount": 30},
        {"amount": 100},  # Нет описания
        {"description": "Taxi ride", "amount": 20},
    ]
    categories = ["restaurant", "taxi"]
    result = process_bank_operations(data, categories)
    assert result == {"restaurant": 1, "taxi": 1}

def test_partial_matches():
    """Проверяет частичное совпадение категории в описании."""
    data = [
        {"description": "Monthly gym subscription", "amount": 40},
        {"description": "Gym equipment", "amount": 200},
    ]
    categories = ["gym"]
    result = process_bank_operations(data, categories)
    assert result == {"gym": 2}

def test_special_characters_in_categories():
    """Проверяет обработку спецсимволов в категориях."""
    data = [
        {"description": "Payment (VIP service)", "amount": 100},
    ]
    categories = ["(VIP"]
    result = process_bank_operations(data, categories)
    assert result == {"(VIP": 1}