import pytest

from src import (
    EmptyExpressionError,
    InvalidNumberInputError,
    InvalidTokenError,
    ParenthesesError,
    RPNExpressionError,
    ZeroDivisionMathError,
)
from src.calculator import opn, remove_parentheses, tokenize_fsm
from src.main import main

"""Проверка нескольких . в числе"""


def test_tokenize_fsm_invalid_number():
    """Тест tokenize_fsm со множеством точек"""
    with pytest.raises(InvalidNumberInputError) as exc_info:
        tokenize_fsm("00.1111.5998")
    assert "Введено несколько точек в числе" in str(exc_info.value)


"""Проверка на некрорректные символы в строке"""


def test_invalid_token():
    with pytest.raises(InvalidTokenError) as exc_info:
        tokenize_fsm("5 5 &")
    assert "Некорректный символ" in str(exc_info.value)


"""Проверка деления на 0"""


def test_zero_division():
    with pytest.raises(ZeroDivisionMathError) as exc_info:
        opn(["5", "0", "//"])
    assert "На ноль делить нельзя!!!" in str(exc_info.value)

    with pytest.raises(ZeroDivisionMathError) as exc_info:
        opn(["10", "0", "%"])
    assert "На ноль делить нельзя!!!" in str(exc_info.value)

    with pytest.raises(ZeroDivisionMathError) as exc_info:
        opn(["5", "0", "/"])
    assert "На ноль делить нельзя!!!" in str(exc_info.value)


"""Тест унарного минуса"""


def test_unarny_minus():
    with pytest.raises(RPNExpressionError) as exc_info:
        opn(["~"])
    assert "Недостаточно операндов для унарного минуса" in str(exc_info.value)


"""Ловим открывающую/закрывающую скобку"""


def test_parentheses():
    with pytest.raises(ParenthesesError) as exc_info:
        remove_parentheses(tokenize_fsm("( 5 3 + "), 0)
    assert "Незакрытая скобка" in str(exc_info.value)

    with pytest.raises(ParenthesesError) as exc_info:
        remove_parentheses(tokenize_fsm("10 2 //)"), 0)
    assert "Лишняя закрывающая скобка" in str(exc_info.value)


def test_empty_expr():
    with pytest.raises(EmptyExpressionError) as exc_info:
        opn("")
    assert "Пустое выражение" in str(exc_info.value)


"""проверка простых операций"""


def test_operation():
    assert float(main("2 2.0001 +")) == 4.0001
    assert float(main("5 2.2 -")) == 2.8
    assert float(main("5 50000 *")) == 250000
    assert float(main("25678 2 /")) == 12839
    assert float(main("502 1 ** ")) == 502
    assert float(main("11 2 //  ")) == 5
    assert float(main("2 -5 *")) == -10


"""проверка сложных операций"""


def test_difficult_opertion():
    assert float(main("2 3 ** 4 5 * + 6 7 % - 8 //")) == 2
    assert float(main("5 2 2 * + 4 5 / - 6 2 ** + 7 8 // - 9 2 % +")) == 45.2
    assert float(main("((2 3 +) (4 5 +) *)")) == 45.0
    assert float(main("(((5 5 +)))5 * ")) == 50
    assert float(main("(((((10 5 + 5 +))))) 2 + 2 *")) == 44
