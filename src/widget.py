from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Маскирует номер карты или счета"""
    if not data or not data.strip():
        raise ValueError("Пустая строка. Ожидается формат: 'Название Номер'")

    parts = data.strip().rsplit(maxsplit=1)
    if len(parts) != 2:
        raise ValueError("Неверный формат данных. Ожидается: 'Название Номер'")

    name, number = parts

    try:
        if "счет" in name.lower():
            return f"{name} {get_mask_account(number)}"
        return f"{name} {get_mask_card_number(number)}"
    except ValueError as e:
        raise ValueError(f"Ошибка маскирования: {str(e)}") from e


def get_date(date_str: str) -> str:
    """Преобразует дату из ISO формата в DD.MM.YYYY"""
    if not date_str or not date_str.strip():
        raise ValueError("Пустая строка с датой")

    if 'T' not in date_str:
        raise ValueError("Неверный формат даты. Ожидается: YYYY-MM-DDThh:mm:ss...")

    date_part = date_str.strip().split('T')[0]

    try:
        year, month, day = date_part.split('-')
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            raise ValueError
        return f"{day}.{month}.{year}"
    except ValueError:
        raise ValueError("Неверный формат даты. Ожидается: YYYY-MM-DDThh:mm:ss...")
