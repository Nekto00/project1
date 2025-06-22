from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счета в строке, сохраняя название продукта.
    Формат ввода: "Название Номер" (например, "Visa Platinum 7000792289606361" или "Счет 73654108430135874305")
    """
    # Разделяем строку на название и номер (берем последнюю часть как номер)
    parts = data.rsplit(maxsplit=1)
    name, number = parts

    # Определяем тип по названию и применяем соответствующую маскировку
    if "счет" in name.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO ("2024-03-11T02:26:18.671407") в формат "ДД.ММ.ГГГГ" ("11.03.2024")
    без использования модуля datetime

    :param date_str: Строка с датой в ISO формате
    :return: Строка с датой в формате "ДД.ММ.ГГГГ"
    :raises ValueError: Если входная строка имеет неверный формат
    """
    try:
        # Разделяем дату и время
        date_part = date_str.split('T')[0]
        year, month, day = date_part.split('-')

        # Проверяем корректность компонентов даты
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            raise ValueError

        # Форматируем в нужный вид
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError):
        raise ValueError(f"Неверный формат даты: {date_str}. Ожидается формат 'YYYY-MM-DDThh:mm:ss...'")
