from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date

print(get_mask_card_number("7000792289606361"))  # Вывод: "7000 79 ** 6361"
print(get_mask_account("73654108430135874305"))   # Вывод: "**4305"
print(mask_account_card("Visa Platinum 7000792289606361"))  # Вывод: "Visa Platinum 7000 79 ** 6361"
print(mask_account_card("Maestro 7000792289606361"))         # Вывод: "Maestro 7000 79 ** 6361"
print(mask_account_card("Счет 73654108430135874305"))   # Вывод: "Счет **4305"
print(get_date("2024-03-11T02:26:18.671407"))  # Вывод: "11.03.2024"
print(get_date("2023-12-31T23:59:59.999999"))  # Вывод: "31.12.2023"
print(get_date("2025-01-01T00:00:00.000000"))  # Вывод: "01.01.2025"