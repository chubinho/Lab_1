from exceptions import (
    InvalidNumberInputError,
    ParenthesesError,
    RPNExpressionError,
    ZeroDivisionMathError,
    TooManyOperandsError,
    EmptyExpressionError,
    InvalidTokenError
)


def tokenize_fsm(expr):
    '''
    Токенизация выражение в ОПН
    '''
    tokens = []
    td = 0
    l = len(expr)

    while td < l:
        '''проходимся по элементам нашего выражения и проверяем, к чему элемент относится(число,пробел,знак операции), пока
        наша переменная не дойдет до конца выражения'''
        char = expr[td]
        if char == ' ':
            td += 1
            continue  # Пробелы игнорируются

        elif char.isdigit():
            """Проверяем, если попалось число. Используем флаг для отображения того, что уже встретили число
            а так же ведем счетчик точек в числе"""

            tek_expr = ""
            has_digit = False
            dot_count = 0

            while td < l and (expr[td].isdigit() or expr[td] == '.'):
                """Собираем число. Проверяем количетсво точек в текущем выражении"""
                if expr[td] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise InvalidNumberInputError(
                            f"Введено несколько точек в числе: '{tek_expr + expr[td]}'")
                else:
                    """Фиксируем, что в выражении уже есть число"""
                    has_digit = True

                """Добавляем текущий элемент в выражение( собираем число ) """
                tek_expr += expr[td]
                td += 1

            if not has_digit or tek_expr.endswith('.'):
                """Если же мы не встретили число или число заканчивается точкой, то выводим ошибку"""
                raise InvalidNumberInputError(
                    f"Некорректное число: '{tek_expr}'")
            try:
                tokens.append(('NUMBER', float(tek_expr)))

            except ValueError:
                raise InvalidNumberInputError(
                    f"Некорректное число: '{tek_expr}'")
            continue

        elif char in '()*/+-%':
            """Проходимся по знакам операций, флаг используем для отметки добавления знака операции"""
            Flag = False
            if td + 1 < l:
                """Проверяем так же, существует ли символ после знака операции, тк можем выйти за длину строки"""
                if char == '/' and expr[td+1] == '/':
                    tokens.append(('OPERATOR', '//'))
                    td += 2
                    Flag = True
                elif char == '*' and expr[td+1] == '*':
                    tokens.append(('OPERATOR', "**"))
                    td += 2
                    Flag = True

            if not Flag and char == '+' and (td == 0 or expr[td-1] in '(+-*/% '):
                """Так же проверяем и унарный минус"""

                if td + 1 < l and (expr[td+1].isdigit() or expr[td+1] == '.'):
                    """Унарный плюс пропускаем"""
                    td += 1
                    continue

            if not Flag and char == '-' and (td == 0 or expr[td-1] in '(+-*/% '):
                """Работаем уже с унарным минусом"""
                if td + 1 < l and (expr[td+1].isdigit() or expr[td+1] == '.'):
                    """Сначала будем работать с числом после унарного минуса,
                    а затем уже добавим и сам минус"""
                    td += 1

                    tek_expr = ""
                    has_digit = False
                    dot_count = 0

                    while td < l and (expr[td].isdigit() or expr[td] == '.'):
                        """Собираем число после унарного минуса"""
                        if expr[td] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                raise InvalidNumberInputError(
                                    f"Введено несколько точек в числе: '{tek_expr + expr[td]}'")
                        else:
                            has_digit = True
                        tek_expr += expr[td]
                        td += 1

                    if not has_digit or tek_expr.endswith('.'):
                        raise InvalidNumberInputError(
                            f"Некорректное число: '{tek_expr}'")

                    try:
                        """Добавляем само число, а потои уже унарный минус"""
                        tokens.append(('NUMBER', float(tek_expr)))
                        tokens.append(('OPERATOR', '~'))
                    except ValueError:
                        raise InvalidNumberInputError(
                            f"Некорректное число: '{tek_expr}'")
                    continue
            if not Flag:
                """Если ничего не добавили, то вносим любой другой опреатор, который не проверяли выше"""
                tokens.append(('OPERATOR', char))
                td += 1
        else:
            raise InvalidTokenError(f'Некорректный символ: "{expr[td]}"')

    return tokens


def is_valid_opn(tokens):
    '''Проверяет, что токены образуют корректный ОПН фрагмент'''
    operand_count = 0
    for token_type, znach in tokens:
        """Проходимся по каждому токену"""
        if token_type == 'NUMBER':
            operand_count += 1
            """При встрече числа, добавляем его в количество общего числа знаков"""
        elif token_type == 'OPERATOR':
            if znach in {'+', '-', '*', '/', '**', '//', '%'}:
                """При встрече знаков операций, проверяем, сколько было уже операндов"""
                if operand_count < 2:
                    return False
                operand_count -= 1
            elif znach == '~':
                """Обрабатываем унарный минус"""
                if operand_count < 1:
                    return False
    return operand_count == 1


def remove_parentheses(tokens, start=0):
    """
    Удаляем скобки с помощью рекурсии
    """
    result = []
    i = start

    while i < len(tokens):
        token_type, znach = tokens[i]

        if znach == '(':
            """обрабатываем содержимое скобок, запускаем рекурсию,
            чтобы проверить корректность выражения внутри"""
            inner_result, new_i = remove_parentheses(tokens, i + 1)

            """Проверяем корректность выражения,
             выводим ошибку, если некорректно """
            if not is_valid_opn(inner_result):
                raise RPNExpressionError(
                    "Некорректное выражение внутри скобок")

            result.extend(inner_result)
            i = new_i

        elif znach == ')':
            """Проверем закрвающую скобку"""
            if start == 0:
                raise ParenthesesError("Лишняя закрывающая скобка")
            """Возвращаем результат и позицию после скобки"""
            return result, i + 1

        else:
            """Если текущий элемент не скобка, то добавляем его в рещультат и смещаемся вправо"""
            result.append((token_type, znach))
            i += 1

    if start > 0:
        raise ParenthesesError("Незакрытая скобка")

    return result


def opn(s):
    """
    Вычисление ОПН выражения, проходимся по токенам
    """
    operator = ['*', '/', '+', '-', '//', '**', '~', '%']
    stack = []

    for symb in s:
        if symb in operator:
            """Обрабатываем именно оператор"""
            if symb == '~':
                """Обрабатываем унарный минус и число с ним"""
                if len(stack) < 1:
                    raise RPNExpressionError(
                        "Недостаточно операндов для унарного минуса")
                try:
                    tek_znach = -float(stack[-1])
                    stack.pop()
                    stack.append(str(tek_znach))
                except:
                    raise RPNExpressionError(
                        "Некорректное выражение с унарным минусом")

            else:
                """Начинаем обработку уже бинарных операций"""
                if len(stack) < 2:
                    raise RPNExpressionError(f"Недостаточно операндов'{symb}'")

                try:
                    b = float(stack[-1])
                    a = float(stack[-2])

                    if symb == '+':
                        tek_znach = a + b
                    elif symb == '-':
                        tek_znach = a - b
                    elif symb == '*':
                        tek_znach = a * b
                    elif symb == '**':
                        tek_znach = a ** b
                    elif symb == '//':
                        if b == 0:
                            raise ZeroDivisionMathError(
                                "На ноль делить нельзя!!!")
                        tek_znach = a // b
                    elif symb == '%':
                        if b == 0:
                            raise ZeroDivisionMathError(
                                "На ноль делить нельзя!!!")
                        tek_znach = a % b
                    elif symb == '/':
                        if b == 0:
                            raise ZeroDivisionMathError(
                                "На ноль делить нельзя!!!")
                        tek_znach = a / b

                    stack.pop()
                    stack.pop()
                    stack.append(str(tek_znach))

                except (ZeroDivisionMathError, RPNExpressionError):
                    """Выводим уже появившиеся ошибки"""
                    raise
                except ValueError:
                    raise RPNExpressionError(
                        "Некорректные операнды")
                except Exception as e:
                    raise RPNExpressionError(f"Ошибка в ОПН: {str(e)}")

        else:
            """Обработка чисел"""
            try:
                float(symb)
                stack.append(symb)
            except ValueError:
                raise InvalidTokenError(f"Некорректный символ '{symb}'")

    if len(stack) == 0:
        raise EmptyExpressionError("Пустое выражение")
    elif len(stack) > 1:
        raise TooManyOperandsError(
            f"В выражении остались лишние операнды: {stack}")

    try:
        """Выводим результат(дополнительно проверяем тип данных)"""
        result = float(stack[0])
        if result.is_integer():
            return str(int(result))
        else:
            return str(result)
    except:
        return stack[0]
