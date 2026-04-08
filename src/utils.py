import json
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Union

from src.external_api import convert_to_rub

# Настройка логгера для модуля transactions
logger = logging.getLogger('transactions')
logger.setLevel(logging.DEBUG)

# Создаем директорию для логов, если её нет
log_dir = Path(__file__).parent.parent / 'logs' / 'utils'
log_dir.mkdir(parents=True, exist_ok=True)

# Создание и настройка file handler
log_file = log_dir / 'transactions.log'
file_handler = logging.FileHandler(log_file, mode='a')
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Добавляем вывод логов в консоль для удобства разработки
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)


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


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список банковских операций, оставляя только те, в описании которых встречается заданная строка.

    Args:
        data: Список словарей с данными о банковских операциях.
        search: Строка для поиска в поле 'description' (регистронезависимый поиск).

    Returns:
        Список словарей, у которых в описании есть искомая строка.
    """
    if not search:
        return data.copy()

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    filtered_data = [item for item in data if 'description' in item and pattern.search(item['description'])]

    return filtered_data


def process_bank_operations(data: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций для каждой указанной категории.

    Args:
        data: Список словарей с данными о банковских операциях.
        categories: Список категорий для поиска в поле 'description' (регистронезависимый поиск).

    Returns:
        Словарь, где ключи — категории, а значения — количество операций в каждой.
        Если категория не найдена, её значение будет 0.
    """
    category_counts = defaultdict(int)

    # Инициализируем все категории с нулями
    for category in categories:
        category_counts[category] = 0

    for operation in data:
        if 'description' not in operation:
            continue

        description = operation['description'].lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    return dict(category_counts)
