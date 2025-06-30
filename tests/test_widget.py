import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для функции маскирования карт и счетов"""

    # Успешные сценарии
    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 1234567890123456", "счет **3456"),
    ])
    def test_valid_input(self, input_data, expected):
        assert mask_account_card(input_data) == expected

    # Тесты на исключения
    def test_empty_input(self):
        with pytest.raises(ValueError, match=".*Пустая строка.*"):
            mask_account_card("")

    def test_missing_number(self):
        with pytest.raises(ValueError, match='Ошибка маскирования: Номер карты должен содержать только цифры'):
            mask_account_card("Visa Platinum")

    def test_invalid_card_number(self):
        with pytest.raises(ValueError, match=".*Ошибка маскирования.*"):
            mask_account_card("Visa Platinum 123")

    def test_invalid_account_number(self):
        with pytest.raises(ValueError, match=".*Ошибка маскирования.*"):
            mask_account_card("Счет 123")


class TestGetDate:
    """Тесты для функции форматирования даты"""

    # Успешные сценарии
    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
    ])
    def test_valid_dates(self, input_date, expected):
        assert get_date(input_date) == expected

    # Тесты на исключения
    def test_empty_date(self):
        with pytest.raises(ValueError, match=".*Пустая строка.*"):
            get_date("")

    def test_invalid_format(self):
        with pytest.raises(ValueError, match=".*Неверный формат.*"):
            get_date("2024/03/11")

    def test_missing_time_part(self):
        with pytest.raises(ValueError, match=".*Неверный формат.*"):
            get_date("2024-03-11")
