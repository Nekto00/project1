def filter_by_state(transactions, state='EXECUTED'):
    """Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions (list): Список словарей для фильтрации.
        state (str, optional): Желаемое значение ключа 'state'. По умолчанию 'EXECUTED'.

    Returns:
        list: Отфильтрованный список словарей.
    """
    return [item for item in transactions if item.get('state') == state]


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
