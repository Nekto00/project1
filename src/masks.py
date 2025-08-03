import logging
import os

# Создаем папку для логов, если её нет
log_dir = os.path.join(os.path.dirname(__file__), '../logs/masks')
os.makedirs(log_dir, exist_ok=True)  # exist_ok=True — не вызывает ошибку, если папка уже есть

# Создание и настройка логгера для модуля masks
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# Создание file handler
file_handler = logging.FileHandler(os.path.join(log_dir, 'masks.log'))

# Создание formatter с требуемым форматом
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Установка formatter для handler
file_handler.setFormatter(file_formatter)

# Добавление handler к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате: 1234 56** **** 5678
    Требования:
    - Минимум 6 цифр
    - Только цифры и пробелы
    - Не пустая строка

    Логирование:
    - DEBUG: Начало обработки
    - INFO: Успешное выполнение
    - ERROR: Ошибки валидации
    """
    try:
        logger.debug(f"Начало обработки номера карты: {card_number}")
        cleaned = card_number.replace(" ", "")

        # Проверки с явным вызовом ValueError
        if not cleaned:
            error_msg = "Номер карты не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)
        if not cleaned.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)
        if len(cleaned) < 6:
            error_msg = "Номер карты должен содержать минимум 6 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматирование номера
        masked_number = (f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
                         if len(cleaned) > 8
                         else f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[6:]}")

        logger.info(f"Успешное маскирование номера карты: {masked_number}")
        return masked_number

    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты {card_number}: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате: **7890
    Требования:
    - Минимум 4 цифры
    - Только цифры и пробелы
    - Не пустая строка

    Логирование:
    - DEBUG: Начало обработки
    - INFO: Успешное выполнение
    - ERROR: Ошибки валидации
    """
    try:
        logger.debug(f"Начало обработки номера счета: {account_number}")
        cleaned = account_number.replace(" ", "")

        # Проверки с явным вызовом ValueError
        if not cleaned:
            error_msg = "Номер счета не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)
        if not cleaned.isdigit():
            error_msg = "Номер счета должен содержать только цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)
        if len(cleaned) < 4:
            error_msg = "Номер счета должен содержать минимум 4 цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_account = f"**{cleaned[-4:]}"
        logger.info(f"Успешное маскирование номера счета: {masked_account}")
        return masked_account

    except Exception as e:
        logger.error(f"Ошибка при маскировании номера счета {account_number}: {str(e)}")
        raise
