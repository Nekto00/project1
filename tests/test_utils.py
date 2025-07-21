import pytest
import requests
from unittest.mock import patch, MagicMock
from src.utils import  get_transaction_amount
from src.external_api import get_exchange_rate, convert_to_rub


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
