import os

import pytest

from src.decorators import log


# Тестовые функции
@log()
def successful_func(a, b):
    return a + b


@log()
def failing_func(a, b):
    return a / b


@log(filename="test_log.txt")
def file_logged_func(a, b):
    return a * b


# Тесты для вывода в консоль
def test_console_log_success(capsys):
    result = successful_func(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "successful_func started" in captured.out
    assert "successful_func ok. Result: 5" in captured.out
    assert "Duration:" in captured.out


def test_console_log_error(capsys):
    with pytest.raises(ZeroDivisionError):
        failing_func(1, 0)

    captured = capsys.readouterr()
    assert "failing_func started" in captured.out
    assert "failing_func error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0)" in captured.out
    assert "Duration:" in captured.out


# Тесты для записи в файл
def test_file_logging():
    # Удаляем предыдущий лог-файл, если он существует
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    result = file_logged_func(3, 4)

    assert result == 12
    assert os.path.exists("test_log.txt")

    with open("test_log.txt", "r") as f:
        content = f.read()
        assert "file_logged_func started" in content
        assert "file_logged_func ok. Result: 12" in content
        assert "Duration:" in content


def test_file_logging_error():
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    with pytest.raises(ZeroDivisionError):
        @log(filename="test_log.txt")
        def div_func(a, b):
            return a / b

        div_func(1, 0)

    assert os.path.exists("test_log.txt")

    with open("test_log.txt", "r") as f:
        content = f.read()
        assert "div_func started" in content
        assert "div_func error: ZeroDivisionError" in content
        assert "Inputs: (1, 0)" in content
        assert "Duration:" in content


# Очистка после тестов
def teardown_module():
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")
