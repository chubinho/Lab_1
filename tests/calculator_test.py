import pytest
from src.main import main

# проверка простых операций


def test_operation():
    assert float(main('2 + 2.0001')) == 4.0001
    assert float(main('5.31 - 2.28')) == 3.03
    assert float(main('5 * 50000')) == 250000
    assert float(main('25678/2')) == 12839

# проверка сложных операций


def test_difficult_opertion():
    assert float(main('10000 / 2 * 10 + 2 * 5 - -5 * -10')) == 49960
    assert float(main('999 / 1 * 100')) == 99900.0
    assert float(main('5 + 3 * 0 - 2')) == 3.0
    assert float(main('2 + 2 * 2')) == 6


# проверка унарных операций
def test_unary_operand():
    res = main('-5 + +40')
    assert float(res) == 35

# проверка деления на 0


def test_division_by_zero():
    """Тест деления на ноль."""
    res = main("5 / 0")
    assert "На ноль делить нельзя" in res

# проверка подряд идущих символов


def test_consecutive_operators():
    res = main("5 + - + 4")
    assert 'Некорректная запись выражения : лишние операнды' in res

# проверка на неподходящие символы в строке


def test_invalid_character():
    res = main('5 & -100000')
    assert 'Неподходящий символ' in res

# Тест пустого выражения


def test_empty_expr():
    res = main('')
    assert 'Выражение без операндов' in res
