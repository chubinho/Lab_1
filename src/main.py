import sys
import os

try:
    # Для запуска: python src/main.py
    from calculator import tokenize_fsm, shunting_yard, opn
except ImportError:
    # Для запуска тестов: python -m pytest
    from .calculator import tokenize_fsm, shunting_yard, opn
# главная функция для вычисления выражения


def main(expr):
    # пробуем разбить на токены, расположить их в ОПН и
    # и вычислить по ходу в ОПН

    try:
        tokens = tokenize_fsm(expr)
        obn = shunting_yard(tokens)
        res = opn(obn)
        return res
    # обрабатыаем ошибку неправильного символа

    except ValueError as a:
        error = str(a)
        if 'Неподходящий символ' in error:
            return error
        # иначе выводим ошибку записи лишних операндов
        else:
            return ('Некорректная запись выражения : лишние операнды')
    # ловим все оставшиеся ошибки
    except Exception:
        return ('Ошибка')

# запускаем алгоритм ввода выражения для пользователя


if __name__ == "__main__":
    expr = input("Введите выражение: ")
    result = main(expr)
    print(result)
