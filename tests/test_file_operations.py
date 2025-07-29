import csv

import pandas as pd # type: ignore
import pytest

from src.file_operations import read_csv, read_excel


@pytest.fixture
def setup_files(tmp_path):
    """Фикстура: создаёт тестовые CSV и Excel файлы."""
    # Тестовые данные
    test_data = [
        {"Дата": "2023-01-01", "Сумма": "1000", "Категория": "Доход"},
        {"Дата": "2023-01-02", "Сумма": "-500", "Категория": "Еда"},
    ]

    # Создаём CSV
    csv_path = tmp_path / "test_transactions.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=test_data[0].keys())
        writer.writeheader()
        writer.writerows(test_data)

    # Создаём Excel
    excel_path = tmp_path / "test_transactions.xlsx"
    df = pd.DataFrame(test_data)
    df.to_excel(excel_path, index=False)

    return csv_path, excel_path  # Возвращаем пути к файлам


def test_csv_transactions(setup_files):
    """Проверяет чтение CSV."""
    csv_path, _ = setup_files
    transactions = read_csv(str(csv_path))

    assert len(transactions) == 2
    assert transactions[0]["Категория"] == "Доход"
    assert transactions[1]["Сумма"] == "-500"


def test_excel_transactions(setup_files):
    """Проверяет чтение Excel."""
    _, excel_path = setup_files
    transactions = read_excel(str(excel_path))

    assert len(transactions) == 2
    assert transactions[0]["Дата"] == "2023-01-01"
    assert transactions[1]["Категория"] == "Еда"


def test_csv_file_not_found():
    """Проверяет ошибку при отсутствии CSV."""
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_file.csv")


def test_excel_file_not_found():
    """Проверяет ошибку при отсутствии Excel."""
    with pytest.raises(FileNotFoundError):
        read_excel("non_existent_file.xlsx")
