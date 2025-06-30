def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате: 1234 56** **** 5678
    Требования:
    - Минимум 6 цифр
    - Только цифры и пробелы
    - Не пустая строка
    """
    cleaned = card_number.replace(" ", "")

    # Проверки с явным вызовом ValueError
    if not cleaned:
        raise ValueError("Номер карты не может быть пустым")
    if not cleaned.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(cleaned) < 6:
        raise ValueError("Номер карты должен содержать минимум 6 цифр")

    # Форматирование номера
    return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}" if len(
        cleaned) > 8 else f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[6:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате: **7890
    Требования:
    - Минимум 4 цифры
    - Только цифры и пробелы
    - Не пустая строка
    """
    cleaned = account_number.replace(" ", "")

    # Проверки с явным вызовом ValueError
    if not cleaned:
        raise ValueError("Номер счета не может быть пустым")
    if not cleaned.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    if len(cleaned) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"**{cleaned[-4:]}"
