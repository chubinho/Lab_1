class MathError(Exception):
    pass


class InvalidNumberInputError(MathError):
    pass


class ParenthesesError(MathError):
    pass


class RPNExpressionError(MathError):
    pass


class ZeroDivisionMathError(MathError):
    pass


class TooManyOperandsError(MathError):
    pass


class EmptyExpressionError(MathError):
    pass


class InvalidTokenError(MathError):
    pass
