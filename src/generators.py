def filter_by_currency(transactions, currency):
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    :param transactions: Список словарей с транзакциями
    :param currency: Код валюты для фильтрации (например, "USD")
    :return: Итератор, который выдает транзакции с заданной валютой
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        transaction_currency = operation_amount.get("currency", {}).get("code")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(transactions):
    """
    Генератор, который возвращает описание каждой транзакции по очереди.
    Если описания нет, возвращает строку "Описание отсутствует".

    :param transactions: Список словарей с транзакциями
    :return: Итератор, который выдает описания транзакций
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start, stop):
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: Начальное значение (от 1 до 9999_9999_9999_9999)
    :param stop: Конечное значение (включительно, >= start)
    :yield: Номер карты в виде строки с пробелами
    """
    for number in range(start, stop + 1):
        # Преобразуем число в 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры и объединяем через пробел
        formatted_card = ' '.join([card_str[i:i + 4] for i in range(0, 16, 4)])
        yield formatted_card
