import functools
from datetime import datetime
from pathlib import Path


def log(filename=None):
    """Декоратор для логирования выполнения функций в файл или консоль.

    Логирует время начала выполнения, длительность, результат (при успешном выполнении)
    или информацию об ошибке (если возникло исключение). Может записывать в файл или выводить в консоль.

    Аргументы:
        filename (str, optional): Путь к файлу для записи логов. Если None, логи выводятся в stdout.

    Возвращает:
        function: Декоратор, оборачивающий исходную функцию логированием.

    Примечание:
        При возникновении исключения оно будет проброшено дальше после логирования.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Автоматически создаем папку для логов, если указан filename
            if filename:
                try:
                    log_path = Path(filename).absolute()
                    log_path.parent.mkdir(parents=True, exist_ok=True)
                    effective_filename = str(log_path)
                except Exception as e:
                    print(f"Ошибка при создании лог-директории: {str(e)}")
                    effective_filename = None
            else:
                effective_filename = None

            # Формируем строку с входными параметрами
            inputs = f"Inputs: {args}, {kwargs}"

            # Логируем начало выполнения функции
            start_time = datetime.now()
            start_msg = f"{func.__name__} started at {start_time}"

            if effective_filename:
                try:
                    with open(effective_filename, 'a', encoding='utf-8') as f:
                        f.write(start_msg + '\n')
                except Exception as e:
                    print(f"Ошибка записи в лог-файл: {str(e)}")
                    print(start_msg)
            else:
                print(start_msg)

            try:
                result = func(*args, **kwargs)
                # Логируем успешное завершение
                end_time = datetime.now()
                duration = end_time - start_time
                success_msg = f"{func.__name__} ok. Result: {result}. Duration: {duration}"

                if effective_filename:
                    try:
                        with open(effective_filename, 'a', encoding='utf-8') as f:
                            f.write(success_msg + '\n')
                    except Exception as e:
                        print(f"Ошибка записи в лог-файл: {str(e)}")
                        print(success_msg)
                else:
                    print(success_msg)

                return result

            except Exception as e:
                # Логируем ошибку
                end_time = datetime.now()
                duration = end_time - start_time
                error_msg = f"{func.__name__} error: {type(e).__name__}: {str(e)}. {inputs}. Duration: {duration}"

                if effective_filename:
                    try:
                        with open(effective_filename, 'a', encoding='utf-8') as f:
                            f.write(error_msg + '\n')
                    except Exception as e:
                        print(f"Ошибка записи в лог-файл: {str(e)}")
                        print(error_msg)
                else:
                    print(error_msg)

                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator


@log(filename="../logs/masks/mylog.txt")
def my_function(x, y):
    return x / y  # Изменил на деление для тестирования ошибок


if __name__ == "__main__":
    # Тест успешного выполнения
    print("Тест успешного выполнения:")
    my_function(4, 2)

    # Тест ошибки
    print("\nТест ошибки:")
    try:
        my_function(1, 0)
    except:
        pass
