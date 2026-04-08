from typing import List, Dict


def filter_by_state(transactions: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """Фильтрует транзакции по статусу с улучшенной обработкой данных.

    Args:
        transactions: Список транзакций (из JSON/CSV/XLSX)
        state: Желаемый статус (регистронезависимый)

    Returns:
        Список отфильтрованных транзакций
    """
    state = state.upper()  # Приводим к верхнему регистру
    filtered = []

    for transaction in transactions:
        try:
            # Получаем статус и приводим к верхнему регистру
            tx_state = str(transaction.get('state', '')).strip().upper()
            if tx_state == state:
                filtered.append(transaction)
        except (AttributeError, KeyError):
            continue

    return filtered


def sort_by_date(transactions, reverse=True):
    """Сортирует список словарей по дате (ключ 'date').

    Args:
        transactions (list): Список словарей для сортировки.
        reverse (bool, optional): Если True — сортировка по убыванию (новые сначала),
                                 иначе — по возрастанию. По умолчанию True.

    Returns:
        list: Отсортированный список словарей.
    """
    return sorted(transactions, key=lambda x: x['date'], reverse=reverse)
