from calculator import opn, remove_parentheses, tokenize_fsm
from exceptions import (
    EmptyExpressionError,
    InvalidNumberInputError,
    InvalidTokenError,
    ParenthesesError,
    RPNExpressionError,
    TooManyOperandsError,
    ZeroDivisionMathError,
)


def main(expr):
    try:
        tokens = tokenize_fsm(expr)
        """ Разбиваем на токены, выводим список с ними"""
        processed_tokens = remove_parentheses(tokens)

        rpn_tokens = []
        for token_type, value in processed_tokens:
            if token_type == "NUMBER":
                if value.is_integer():
                    rpn_tokens.append(str(int(value)))
                else:
                    rpn_tokens.append(str(value))
            else:
                rpn_tokens.append(value)

        result = opn(rpn_tokens)

        return result

    except InvalidNumberInputError as e:
        return f"Ошибка ввода неправильного числа: {e}"
    except ParenthesesError as e:
        return f"Ошибка скобок: {e}"
    except RPNExpressionError as e:
        return f"Ошибка выражения: {e}"
    except ZeroDivisionMathError as e:
        return f"Ошибка деления на 0: {e}"
    except TooManyOperandsError as e:
        return f"Ошибка выражения перебора операндов: {e}"
    except EmptyExpressionError as e:
        return f"Ошибка выражения: {e}"
    except InvalidTokenError as e:
        return f"Ошибка ввода: {e}"
    except Exception as e:
        return f"Неизвестная ошибка: {e}"


if __name__ == "__main__":
    expr = input("Введите выражение: ")
    result = main(expr)
    print(result)
