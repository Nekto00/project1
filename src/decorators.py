import functools
from datetime import datetime


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем строку с входными параметрами
            inputs = f"Inputs: {args}, {kwargs}"

            # Логируем начало выполнения функции
            start_time = datetime.now()
            start_msg = f"{func.__name__} started at {start_time}"

            if filename:
                with open(filename, 'a') as f:
                    f.write(start_msg + '\n')
            else:
                print(start_msg)

            try:
                result = func(*args, **kwargs)
                # Логируем успешное завершение
                end_time = datetime.now()
                duration = end_time - start_time
                success_msg = f"{func.__name__} ok. Result: {result}. Duration: {duration}"

                if filename:
                    with open(filename, 'a') as f:
                        f.write(success_msg + '\n')
                else:
                    print(success_msg)

                return result

            except Exception as e:
                # Логируем ошибку
                end_time = datetime.now()
                duration = end_time - start_time
                error_msg = f"{func.__name__} error: {type(e).__name__}: {str(e)}. {inputs}. Duration: {duration}"

                if filename:
                    with open(filename, 'a') as f:
                        f.write(error_msg + '\n')
                else:
                    print(error_msg)

                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)