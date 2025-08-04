import sys
import json
import csv
import openpyxl
from typing import List, Dict, Union
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions, process_bank_search
from src.file_operations import read_csv, read_excel
from src.masks import get_mask_account, get_mask_card_number


def filter_rub_transactions(transactions: List[Dict]) -> List[Dict]:
    """
    Фильтрует список транзакций, оставляя только рублёвые (RUB).

    Args:
        transactions: Список словарей с транзакциями, где каждый словарь содержит:
            - 'amount' (число или строка)
            - 'currency' (строка, опционально - по умолчанию считается RUB)

    Returns:
        Список транзакций только с рублёвыми операциями

    Пример:
        transactions = [
        ...     {'amount': 100, 'currency': 'RUB'},
        ...     {'amount': 50, 'currency': 'USD'},
        ...     {'amount': 200}  # Будет считаться RUB по умолчанию
        ... ]
        filter_rub_transactions(transactions)
        [{'amount': 100, 'currency': 'RUB'}, {'amount': 200}]
    """
    rub_transactions = []

    for transaction in transactions:
        try:
            # Получаем валюту, по умолчанию RUB
            currency = str(transaction.get('currency', 'RUB')).upper()

            # Проверяем, что валюта рубль (допускаются варианты: RUB, руб, RUR и т.д.)
            if currency in ('RUB', 'РУБ', 'RUR'):
                rub_transactions.append(transaction)

        except (AttributeError, TypeError) as e:
            # Пропускаем транзакции с некорректными данными
            continue

    return rub_transactions


def safe_convert(value: Union[str, float, int]) -> float:
    """Безопасное преобразование в число"""
    if isinstance(value, (float, int)):
        return float(value)
    try:
        # Удаляем пробелы и заменяем запятые на точки
        cleaned = str(value).replace(' ', '').replace(',', '.')
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0


def print_transaction(transaction: Dict) -> None:
    """Универсальный вывод транзакции"""
    try:
        # Преобразуем все значения в строки для безопасности
        date = str(transaction.get('date', 'Нет данных')).strip()
        description = str(transaction.get('description', 'Без описания')).strip()
        print(f"\n{date} {description}")

        # Обработка from/to с защитой от ошибок
        for direction in ['from', 'to']:
            if direction in transaction:
                value = str(transaction[direction])
                if any(word in value.lower() for word in ['карта', 'card']):
                    parts = value.rsplit(' ', 1)
                    masked = f"{parts[0]} {get_mask_card_number(parts[1])}" if len(parts) == 2 else value
                else:
                    parts = value.rsplit(' ', 1)
                    masked = f"{parts[0]} {get_mask_account(parts[1])}" if len(parts) == 2 else value
                print(masked, end=' -> ' if direction == 'from' else '\n')

        # Обработка суммы
        amount = safe_convert(transaction.get('amount', 0))
        currency = str(transaction.get('currency', 'RUB')).upper()
        print(f"Сумма: {amount:.2f} {currency}")

    except Exception as e:
        print(f"\nОшибка при выводе транзакции: {str(e)}")
        print(f"Сырые данные: {transaction}")


def load_json(filepath: str) -> List[Dict]:
    """Загрузка JSON файла с обработкой всех форматов"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        return [data]
    return data


def load_csv(filepath: str) -> List[Dict]:
    """Загрузка CSV файла с правильным парсингом"""
    transactions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Конвертируем все значения в строки
            cleaned = {k: str(v).strip() for k, v in row.items()}
            transactions.append(cleaned)
    return transactions


def load_xlsx(filepath: str) -> List[Dict]:
    """Загрузка XLSX с обработкой числовых значений"""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]

    transactions = []
    for row in ws.iter_rows(min_row=2):
        transaction = {}
        for header, cell in zip(headers, row):
            value = cell.value
            # Преобразуем числа в строки для единообразия
            transaction[header] = str(value) if value is not None else ''
        transactions.append(transaction)
    return transactions


def process_file(filepath: str) -> None:
    """Обработка файла любого формата"""
    if filepath.endswith('.json'):
        transactions = load_json(filepath)
    elif filepath.endswith('.csv'):
        transactions = load_csv(filepath)
    elif filepath.endswith('.xlsx'):
        transactions = load_xlsx(filepath)
    else:
        raise ValueError("Неподдерживаемый формат файла")

    for idx, tx in enumerate(transactions, 1):
        print(f"\nТранзакция #{idx}:")
        print_transaction(tx)
        print("-" * 40)


def display_transactions(transactions: List[Dict]) -> None:
    """Выводит список транзакций с заголовком"""
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for transaction in transactions:
        print_transaction(transaction)
        print()


def file_tip_transactions(filename: str, file_type: str) -> List[Dict]:
    """Загружает транзакции в зависимости от типа файла"""
    try:
        if file_type == '1':
            return load_transactions(filename)
        elif file_type == '2':
            return read_csv(filename)
        elif file_type == '3':
            return read_excel(filename)
    except Exception as e:
        raise Exception(f"Ошибка загрузки файла: {str(e)}")


def get_valid_input(prompt: str, valid_options: list) -> str:
    """Получает корректный ввод от пользователя"""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Ошибка: допустимые варианты - {', '.join(valid_options)}")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Шаг 1: Выбор типа файла
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_type = get_valid_input("Ваш выбор (1-3): ", ['1', '2', '3'])
    filename = input("Введите путь к файлу: ")

    try:
        # Шаг 2: Загрузка данных
        transactions = file_tip_transactions(filename, file_type)
        file_types = {
            '1': 'JSON',
            '2': 'CSV',
            '3': 'XLSX'
        }
        print(f"\nДля обработки выбран {file_types[file_type]}-файл.")
    except FileNotFoundError:
        print("\nОшибка: указанный файл не найден", file=sys.stderr)
        return
    except Exception as e:
        print(f"\n{e}", file=sys.stderr)
        return

    # Шаг 3: Фильтрация по статусу
    valid_statuses = ['executed', 'canceled', 'pending']
    while True:
        status = input("\nВведите статус (EXECUTED/CANCELED/PENDING): ").strip().lower()
        if status in valid_statuses:
            filtered = filter_by_state(transactions, status.upper())
            print(f"\nОперации отфильтрованы по статусу \"{status.upper()}\"")
            break
        print(f"\nСтатус операции \"{status}\" недоступен.")

    # Шаг 4: Дополнительные фильтры
    if get_valid_input("\nОтсортировать по дате? (да/нет): ", ['да', 'нет']) == 'да':
        order = get_valid_input("По возрастанию или убыванию? (возрастанию/убыванию): ",
                                ['возрастанию', 'убыванию'])
        filtered = sort_by_date(filtered, reverse=(order == 'убыванию'))

    if get_valid_input("\nТолько рублевые транзакции? (да/нет): ", ['да', 'нет']) == 'да':
        filtered = filter_rub_transactions(filtered)

    if get_valid_input("\nФильтровать по слову в описании? (да/нет): ", ['да', 'нет']) == 'да':
        search_word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, search_word)

    # Шаг 5: Вывод результатов
    print(display_transactions(filtered))

if __name__ == "__main__":
    main()