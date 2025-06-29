from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

print(get_mask_card_number("7000792289606361"))  # Вывод: "7000 79 ** 6361"
print(get_mask_account("73654108430135874305"))   # Вывод: "**4305"
print(mask_account_card("Visa Platinum 7000792289606361"))  # Вывод: "Visa Platinum 7000 79 ** 6361"
print(mask_account_card("Maestro 7000792289606361"))         # Вывод: "Maestro 7000 79 ** 6361"
print(mask_account_card("Счет 73654108430135874305"))   # Вывод: "Счет **4305"
print(get_date("2024-03-11T02:26:18.671407"))  # Вывод: "11.03.2024"
print(get_date("2023-12-31T23:59:59.999999"))  # Вывод: "31.12.2023"
print(get_date("2025-01-01T00:00:00.000000"))  # Вывод: "01.01.2025"

data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Фильтрация по умолчанию (EXECUTED)
print(filter_by_state(data))
# [{'id': 41428829, ...}, {'id': 939719570, ...}]

# Фильтрация по CANCELED
print(filter_by_state(data, 'CANCELED'))
# [{'id': 594226727, ...}, {'id': 615064591, ...}]

# Сортировка по убыванию (новые операции в начале)
print(sort_by_date(data))
# [
#    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
#    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
# ]

# Сортировка по возрастанию (старые операции в начале)
print(sort_by_date(data, reverse=False))
# [
#    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
#    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
# ]
