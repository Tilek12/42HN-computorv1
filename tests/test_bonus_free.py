import pytest

from parser import parse_equation
from parser_free import parse_equation_free


def test_free_accepts_subject_bonus_example():
    lhs, rhs = parse_equation_free("5 + 4 * X + X^2 = X^2")
    assert lhs == [(5.0, 0), (4.0, 1), (1.0, 2)]
    assert rhs == [(1.0, 2)]


def test_free_accepts_compact_form_without_spaces():
    lhs, rhs = parse_equation_free("2X^2-3X+1=0")
    assert lhs == [(2.0, 2), (-3.0, 1), (1.0, 0)]
    assert rhs == [(0.0, 0)]


def test_free_accepts_implicit_coeff_and_power():
    lhs, rhs = parse_equation_free("-X^2+X-7=0")
    assert lhs == [(-1.0, 2), (1.0, 1), (-7.0, 0)]
    assert rhs == [(0.0, 0)]


def test_free_accepts_decimal_coefficients():
    lhs, rhs = parse_equation_free("3.5X-1.2=0")
    assert lhs == [(3.5, 1), (-1.2, 0)]
    assert rhs == [(0.0, 0)]


def test_free_accepts_x_equals_constant():
    lhs, rhs = parse_equation_free("X=5")
    assert lhs == [(1.0, 1)]
    assert rhs == [(5.0, 0)]


def test_dispatch_mode_free_works():
    lhs, rhs = parse_equation("X=5", mode="free")
    assert lhs == [(1.0, 1)]
    assert rhs == [(5.0, 0)]


def test_dispatch_unknown_mode_raises():
    with pytest.raises(ValueError, match="Unknown parser mode"):
        parse_equation("X=5", mode="unknown")


@pytest.mark.parametrize(
    "equation, message",
    [
        ("", "must not be empty"),
        ("   ", "must not be empty"),
        ("X=1=2", "exactly one '='"),
        ("=X", "Left side is empty"),
        ("X=", "Right side is empty"),
        ("2x+1=0", "uppercase 'X'"),
        ("X^-2=0", "Negative exponents"),
        ("X^1.5=0", "Exponent must be a non-negative integer"),
        ("2**X^2=0", "Invalid operator sequence"),
        ("2//X=0", "Invalid operator sequence"),
        ("X+ = 0", "trailing operator"),
        ("@ + X = 0", "Invalid character"),
    ],
)


def test_free_invalid_cases(equation: str, message: str):
    with pytest.raises(ValueError, match=message):
        parse_equation_free(equation)
