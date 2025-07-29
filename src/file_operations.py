import csv
from typing import Dict, List

import pandas as pd # type: ignore


def read_csv(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из CSV-файла и возвращает список словарей с транзакциями.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        List[Dict]: Список транзакций, где каждая транзакция представлена словарем.
    """
    transactions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            transactions.append(dict(row))
    return transactions


def read_excel(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из Excel-файла и возвращает список словарей с транзакциями.

    Args:
        file_path (str): Путь к Excel-файлу.

    Returns:
        List[Dict]: Список транзакций, где каждая транзакция представлена словарем.
    """
    df = pd.read_excel(file_path)
    transactions = df.to_dict('records')
    return transactions
