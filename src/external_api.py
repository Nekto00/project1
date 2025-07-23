import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> float:
    """Получает текущий курс валюты к рублю."""
    if not API_KEY:
        raise ValueError("API key not configured in environment variables")

    response = requests.get(
        BASE_URL,
        params={"base": base_currency, "symbols": target_currency},
        headers={"apikey": API_KEY}
    )
    response.raise_for_status()
    data = response.json()
    return data["rates"][target_currency]


def convert_to_rub(amount: float, currency: str) -> float:
    """Конвертирует сумму в рубли по текущему курсу."""
    if currency == "RUB":
        return amount

    rate = get_exchange_rate(currency)
    return round(amount * rate, 2)
