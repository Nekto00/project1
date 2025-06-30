import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestMaskCardNumber:
    """Тесты для маскирования номеров карт"""

    def test_standard_16_digit(self, numbers):
        assert get_mask_card_number("1234567812345678") == numbers

    def test_with_spaces(self, numbers_unusual):
        assert get_mask_card_number("1234 5678 1234 5678") == numbers_unusual

    def test_short_number_10_digits(self, numbers_short):
        assert get_mask_card_number("1234567890") == numbers_short

    def test_short_number_raises_error(self):
        """Проверка, что номер короче 6 цифр вызывает ошибку"""
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("12345")
        assert "минимум 6 цифр" in str(excinfo.value)

    def test_empty_input_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("")
        assert "не может быть пустым" in str(excinfo.value)

    def test_non_digit_input_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_card_number("1234abcd5678")
        assert "только цифры" in str(excinfo.value)


class TestMaskAccount:
    """Тесты для маскирования номеров счетов"""

    def test_standard_account(self, numbers_account):
        assert get_mask_account("1234567890") == numbers_account

    def test_with_spaces(self, numbers_account):
        assert get_mask_account("1234 5678 90") == numbers_account

    def test_short_account_4_digits(self, numbers_account_short):
        assert get_mask_account("1234") == numbers_account_short

    def test_short_account_raises_error(self):
        """Проверка, что номер короче 4 цифр вызывает ошибку"""
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("123")
        assert "минимум 4 цифры" in str(excinfo.value)

    def test_empty_input_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("")
        assert "не может быть пустым" in str(excinfo.value)

    def test_non_digit_input_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            get_mask_account("acc1234")
        assert "только цифры" in str(excinfo.value)
