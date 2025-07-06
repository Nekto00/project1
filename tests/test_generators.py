import pytest
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200",
                "currency": {"code": "EUR"}
            }
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "300",
                "currency": {"code": "USD"}
            }
        },
        {"id": 4},  # Транзакция без operationAmount
        {
            "id": 5,
            "operationAmount": {
                "amount": "500",
                "currency": {}  # Транзакция с пустым currency
            }
            # нет поля description
        }
    ]


def test_filter_by_currency_usd(sample_transactions):
    """Тест фильтрации транзакций в USD."""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert all(t["id"] in {1, 3} for t in usd_transactions)


def test_filter_by_currency_eur(sample_transactions):
    """Тест фильтрации транзакций в EUR."""
    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 2


def test_filter_by_currency_empty_result(sample_transactions):
    """Тест случая, когда подходящих транзакций нет."""
    gbp_transactions = list(filter_by_currency(sample_transactions, "GBP"))
    assert len(gbp_transactions) == 0


def test_filter_by_currency_empty_input():
    """Тест обработки пустого списка транзакций."""
    empty_transactions = list(filter_by_currency([], "USD"))
    assert len(empty_transactions) == 0


@pytest.mark.parametrize("currency, expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2]),
    ("GBP", []),
])
def test_filter_by_currency_parametrized(sample_transactions, currency, expected_ids):
    """Параметризованный тест для разных валют."""
    transactions = list(filter_by_currency(sample_transactions, currency))
    assert [t["id"] for t in transactions] == expected_ids



def test_transaction_descriptions_normal_cases(sample_transactions):
    """Тест корректного возврата описаний для стандартных транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = [
        "Описание отсутствует",
        "Описание отсутствует",
        "Описание отсутствует",
        "Описание отсутствует",
        "Описание отсутствует"
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_input():
    """Тест обработки пустого списка транзакций."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


@pytest.mark.parametrize("transactions, expected", [
    ([], []),
    (
        [{"description": "Оплата услуг"}],
        ["Оплата услуг"]
    ),
    (
        [{"id": 1}, {"description": "Перевод"}],
        ["Описание отсутствует", "Перевод"]  # Первая транзакция без description
    ),
    (
        [{"id": 1, "description": "Описание отсутствует"}],  # Явный None в description
        ["Описание отсутствует"]
    ),
])
def test_transaction_descriptions_parametrized(transactions, expected):
    """Параметризованный тест для разных входных данных."""
    result = list(transaction_descriptions(transactions))
    assert result == expected


def test_transaction_descriptions_all_none():
    """Тест случая, когда ни у одной транзакции нет описания."""
    transactions = [{"id": 1}, {"id": 2}]
    assert list(transaction_descriptions(transactions)) == ["Описание отсутствует", "Описание отсутствует"]

    @pytest.mark.parametrize("start, end, expected", [
        # Стандартные случаи
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]),
        # Крайние значения
        (9999999999999998, 9999999999999999, [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999"
        ]),
        # Диапазон из одного элемента
        (1234123412341234, 1234123412341234, [
            "1234 1234 1234 1234"
        ]),
        # Большие числа
        (1000000000000000, 1000000000000002, [
            "1000 0000 0000 0000",
            "1000 0000 0000 0001",
            "1000 0000 0000 0002"
        ]),
    ])
    def test_card_number_generator_range(start, end, expected):
        """Тест генерации номеров карт в заданном диапазоне."""
        result = list(card_number_generator(start, end))
        assert result == expected

    def test_card_number_generator_format():
        """Тест корректности форматирования номеров карт."""
        numbers = list(card_number_generator(1234567812345678, 1234567812345678))
        assert numbers[0] == "1234 5678 1234 5678"
        assert len(numbers[0]) == 19  # 16 цифр + 3 пробела

    def test_card_number_generator_empty_range():
        """Тест обработки некорректного диапазона (start > end)."""
        with pytest.raises(ValueError):
            list(card_number_generator(5, 1))

    def test_card_number_generator_edge_values():
        """Тест обработки крайних значений диапазона."""
        # Минимальное значение
        min_val = list(card_number_generator(1, 1))
        assert min_val == ["0000 0000 0000 0001"]

        # Максимальное значение
        max_val = list(card_number_generator(9999999999999999, 9999999999999999))
        assert max_val == ["9999 9999 9999 9999"]

    def test_card_number_generator_large_range():
        """Тест производительности на большом диапазоне."""
        gen = card_number_generator(1, 1000)
        first = next(gen)
        last = None
        for last in gen:
            pass
        assert first == "0000 0000 0000 0001"
        assert last == "0000 0000 0000 1000"