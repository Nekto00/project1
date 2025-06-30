import pytest
from src.processing import filter_by_state, sort_by_date


# Тестовые данные
SAMPLE_TRANSACTIONS = [
    {'state': 'EXECUTED', 'date': '2023-05-01T12:00:00.000'},
    {'state': 'PENDING', 'date': '2023-05-02T12:00:00.000'},
    {'state': 'EXECUTED', 'date': '2023-05-03T12:00:00.000'},
    {'state': 'CANCELED', 'date': '2023-05-01T12:00:00.000'},  # Та же дата, что и у первого
    {'state': 'EXECUTED', 'date': '2023-01-01T00:00:00.000'},
]

# Тесты для filter_by_state


class TestFilterByState:
    @pytest.mark.parametrize('state,expected_count', [
        ('EXECUTED', 3),
        ('PENDING', 1),
        ('CANCELED', 1),
        ('UNKNOWN', 0),
    ])
    def test_filter_by_state(self, state, expected_count):
        """Тестирует фильтрацию по различным статусам."""
        result = filter_by_state(SAMPLE_TRANSACTIONS, state)
        assert len(result) == expected_count
        assert all(item['state'] == state for item in result)

    def test_default_state(self):
        """Тестирует фильтрацию со статусом по умолчанию (EXECUTED)."""
        result = filter_by_state(SAMPLE_TRANSACTIONS)
        assert len(result) == 3
        assert all(item['state'] == 'EXECUTED' for item in result)

# Тесты для sort_by_date


class TestSortByDate:
    def test_sort_descending(self):
        """Тестирует сортировку по убыванию даты (новые сначала)."""
        result = sort_by_date(SAMPLE_TRANSACTIONS, reverse=True)
        dates = [item['date'] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_ascending(self):
        """Тестирует сортировку по возрастанию даты (старые сначала)."""
        result = sort_by_date(SAMPLE_TRANSACTIONS, reverse=False)
        dates = [item['date'] for item in result]
        assert dates == sorted(dates)

    def test_same_dates(self):
        """Тестирует корректность сортировки при одинаковых датах."""
        # Создаем список с одинаковыми датами
        same_date_transactions = [
            {'date': '2023-05-01T12:00:00.000', 'id': 1},
            {'date': '2023-05-01T12:00:00.000', 'id': 2},
            {'date': '2023-05-01T12:00:00.000', 'id': 3},
        ]
        result = sort_by_date(same_date_transactions, reverse=True)
        # Проверяем, что порядок элементов сохранился (стабильная сортировка)
        assert [item['id'] for item in result] == [1, 2, 3]

    @pytest.mark.parametrize('date', [
        'invalid-date',
        '2023-13-01T00:00:00.000',  # Неверный месяц
        '2023-05-32T00:00:00.000',  # Неверный день
        '2023/05/01 00:00:00',     # Неправильный формат
    ])
    def test_invalid_dates(self, date):
        """Тестирует обработку невалидных форматов дат."""
        # Функция просто пытается отсортировать как строки
        # В этом случае исключений не будет, но сортировка может быть некорректной
        result = sort_by_date([{'date': date}])
        assert len(result) == 1

    def test_non_string_date(self):
        """Тестирует обработку даты не в строковом формате."""
        # Для нестроковых значений может возникнуть TypeError при сравнении
        with pytest.raises(TypeError):
            sort_by_date([{'date': 12345}, {'date': '2023-01-01T00:00:00.000'}])
