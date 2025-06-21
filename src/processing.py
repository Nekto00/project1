def filter_by_state(transactions, state='EXECUTED'):
    """Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions (list): Список словарей для фильтрации.
        state (str, optional): Желаемое значение ключа 'state'. По умолчанию 'EXECUTED'.

    Returns:
        list: Отфильтрованный список словарей.
    """
    return [item for item in transactions if item.get('state') == state]