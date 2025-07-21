import json
from pathlib import Path
from src.external_api import  convert_to_rub


def load_transactions(file_path):
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    :param file_path: Путь до JSON-файла с транзакциями
    :return: Список словарей с данными о транзакциях или пустой список, если файл не найден, пуст или содержит не список
    """
    try:
        # Проверяем существование файла
        if not Path(file_path).exists():
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, FileNotFoundError):
        # Обрабатываем случаи, когда файл пустой или невалидный JSON
        return []


def get_transaction_amount(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount = float(transaction["amount"])
    currency = transaction.get("currency", "RUB")

    if currency not in ("RUB", "USD", "EUR"):
        raise ValueError(f"Unsupported currency: {currency}")

    return convert_to_rub(amount, currency)
