def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 цифры, заменяя остальные на *."""
    # Удаляем все пробелы (если есть) и проверяем, что номер состоит из цифр
    cleaned_number = card_number.replace(" ", "")
    # Форматируем номер: первые 6 цифр + последние 4, остальные заменяем на *
    masked_part = "****"
    formatted_number = f"{cleaned_number[:4]} {cleaned_number[4:6]}** {masked_part} {cleaned_number[-4:]}"
    return formatted_number


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета, оставляя только последние 4 цифры, заменяя первые на **."""
    # Удаляем все пробелы (если есть) и проверяем, что номер состоит из цифр
    cleaned_number = account_number.replace(" ", "")
    # Форматируем номер: ** + последние 4 цифры
    return f"**{cleaned_number[-4:]}"
