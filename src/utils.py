import json
import logging
from pathlib import Path
from typing import Dict, List, Union

from src.external_api import convert_to_rub

# Настройка логгера для модуля transactions
logger = logging.getLogger('transactions')
logger.setLevel(logging.DEBUG)

# Создание и настройка file handler
file_handler = logging.FileHandler('../logs/utils/transactions.log', mode='a')
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    Логирует:
    - DEBUG: Начало загрузки файла
    - INFO: Успешная загрузка (с количеством транзакций)
    - WARNING: Файл не найден или пустой
    - ERROR: Ошибки при обработке файла

    :param file_path: Путь до JSON-файла с транзакциями
    :return: Список словарей с данными о транзакциях или пустой список
    """
    try:
        logger.debug(f"Начало загрузки файла: {file_path}")
        path = Path(file_path)

        if not path.exists():
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.warning(f"Файл {file_path} не содержит список транзакций")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при обработке файла {file_path}: {str(e)}")
        return []


def get_transaction_amount(transaction: Dict) -> float:
    """
    Возвращает сумму транзакции в рублях.
    Логирует:
    - DEBUG: Начало обработки транзакции
    - INFO: Успешный расчет суммы
    - ERROR: Ошибки валидации или конвертации

    :param transaction: Словарь с данными о транзакции
    :return: Сумма транзакции в рублях
    :raises: ValueError при неподдерживаемой валюте
    """
    try:
        logger.debug(f"Обработка транзакции: {transaction.get('id', 'без ID')}")

        amount = float(transaction["amount"])
        currency = transaction.get("currency", "RUB")

        if currency not in ("RUB", "USD", "EUR"):
            error_msg = f"Неподдерживаемая валюта: {currency}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        rub_amount = convert_to_rub(amount, currency)
        logger.info(f"Успешный расчет суммы: {amount} {currency} = {rub_amount} RUB")
        return rub_amount

    except KeyError as e:
        error_msg = f"Отсутствует обязательное поле в транзакции: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except (TypeError, ValueError) as e:
        error_msg = f"Ошибка конвертации суммы: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Непредвиденная ошибка при обработке транзакции: {str(e)}"
        logger.error(error_msg)
        raise
