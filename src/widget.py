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