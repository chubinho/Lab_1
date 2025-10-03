def tokenize_fsm(expr):  # разбиение на токены
    tokens = []
    state = 'START'  # состояние для начала токенизации, а также это состояние начинает работать при окончании слова
    current_token = ''

    # проходимся по элементам нашего выражения и проверяем, к чему элемент относится(число,пробел,знак операции)
    for char in expr:
        if char == ' ':

            continue  # пробелы игнорируются
        if state == 'START':
            if char.isdigit():  # если элемент число - с него начинается токен
                state = 'NUMBER'
                current_token = char
            elif char == '+' or char == '-':  # учитываем унарные "+" и "-" перед числом
                state = 'NUMBER'
                current_token = char
            else:
                raise ValueError('Неподходящий символ')

        elif state == 'NUMBER':  # собираем число
            if char.isdigit():
                current_token += char
            elif char == '.':  # собираем десятичное число
                state = 'POINT'  # для этого переходим в состояние POINT и собираем часть после "."
                current_token += char
            elif char in ['+', '-', '*', '/']:
                # когда встречаем знак операции, то добавляем само число(токен),
                # а потом сам знак операции(токен)
                try:
                    float(current_token)

                    tokens.append(('NUMBER', float(current_token)))
                    current_token = ''
                    state = 'START'
                    tokens.append(('OPERATOR', char))
                except ValueError:
                    raise ValueError('Неправильная запись выражения')
            else:
                raise ValueError('Неподходящий символ')

        elif state == 'POINT':  # собираем число после "." и прибавляем к текущему числу
            if char.isdigit():
                current_token += char

            # когда встречаем знак операции, то добавляем само число(токен), а потом сам знак операции(токен)
            elif char in ['+', '-', '*', '/']:
                tokens.append(('NUMBER', float(current_token)))
                current_token = ''
                state = 'START'
                tokens.append(('OPERATOR', char))

    if state == 'NUMBER' or state == 'POINT':  # добавляем последнее число в токен
        # проверяем, не является ли текущий токен просто знаком операции
        try:
            num = float(current_token)
            tokens.append(('NUMBER', float(current_token)))
        except ValueError:
            raise ValueError('Неправильная запись выражения')

    return tokens


# через класс Stack мы реализуем работу с токеном и перевод в строки в опн


class Stack:
    def __init__(self):  # создаём список(стэк), куда будут вноситься токены
        self.items = []

    def push(self, item):  # заносим токен в конец стэка
        self.items.append(item)

    def pop(self):  # убираем элемент "сверху" стэка и выводим его
        return self.items.pop()

    def is_empty(self):  # проверяем, пуст ли стэк
        return (self.items == [])

# функция перевода в ОПЗ


def shunting_yard(tokens):
    stack_operator = Stack()  # задаем тип данных Stack
    output = []  # вывод
    prioritet = {'+': 1, '-': 1, '*': 2, '/': 2}  # приоритеты знаков операции

    for token in tokens:  # проходимся по токенам
        if token[0] == 'NUMBER':
            # если токен это число, то сразу заносим в вывод
            output.append(str(token[1]))
        elif token[0] == 'OPERATOR':
            current_operator = token[1]
            while not stack_operator.is_empty() and \
                    prioritet[stack_operator.items[-1]] >= prioritet[current_operator]:  # проверяем, не пуст ли стэк и
                # сравниваем приоритеты знаков операции(сравниваем со всеми знаками в стэке)
                # если приоритет текущего оператора <= крайнего,
                last_operator = stack_operator.pop()
                # то выталкиваем крайний оператор стэка
                output.append(last_operator)

            # заносим текущий оператор в стэк
            stack_operator.push(current_operator)
    while not stack_operator.is_empty():  # заносим в вывод жо того момента, пока стэк не станет пустым
        output.append(stack_operator.pop())
    return output  # возвращаем вывод(ОПН)


# обрабатываем ОПН и считаем в правильном порядке


def opn(s):
    operator = ['*', '/', '+', '-']
    stack = []
    for symb in s:  # проходимся по элементам ОПН
        if symb in operator:
            try:

                if symb == '+':  # если "+", то выполнем операцию и запоминаем ответ
                    tek_znach = float(stack[-2]) + float(stack[-1])
                    stack.pop()
                    stack.pop()

                elif symb == '-':  # если "-", то выполнем операцию и запоминаем ответ
                    tek_znach = float(stack[-2]) - float(stack[-1])
                    stack.pop()
                    stack.pop()

                elif symb == '*':  # если "*", то выполнем операцию и запоминаем ответ
                    tek_znach = float(stack[-2]) * float(stack[-1])
                    stack.pop()
                    stack.pop()

                try:
                    if symb == '/':  # если "/", то выполнем операцию и запоминаем ответ
                        tek_znach = float(stack[-2]) / float(stack[-1])
                        stack.pop()
                        stack.pop()
                except ZeroDivisionError:
                    return ('На ноль делить нельзя!!!')

                stack.append(str(tek_znach))  # вносим ответ в стэк
            except IndexError:
                return 'Недостаточно элементов в стэке'

        else:
            try:
                # проверяем число
                float(symb)
                stack.append(symb)
            except ValueError:
                return "Неподходящий символ"
    if len(stack) != 1:
        return 'Выражение без операндов'

    return stack[0]
