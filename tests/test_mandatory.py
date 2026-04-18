import pytest

from parser import parse_equation
from reducer import reduce_terms, polynomial_degree
from solver import solve_polynomial
from math_utils import ft_abs


def solve(eq: str):
    lhs, rhs = parse_equation(eq)
    coeffs = reduce_terms(lhs, rhs)
    degree = polynomial_degree(coeffs)
    result = solve_polynomial(coeffs, degree)
    return degree, result


def test_degree_1():
    degree, result = solve("5 * X^0 + 4 * X^1 = 4 * X^0")
    assert degree == 1
    assert result["kind"] == "one_real"
    assert ft_abs(result["x"] + 0.25) < 1e-9


def test_all_real():
    degree, result = solve("6 * X^0 = 6 * X^0")
    assert degree == 0
    assert result["kind"] == "all_real"


def test_no_solution():
    degree, result = solve("10 * X^0 = 15 * X^0")
    assert degree == 0
    assert result["kind"] == "no_solution"


def test_two_real():
    degree, result = solve("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    assert degree == 2
    assert result["kind"] == "two_real"


def test_two_complex():
    degree, result = solve("1 * X^0 + 2 * X^1 + 5 * X^2 = 0 * X^0")
    assert degree == 2
    assert result["kind"] == "two_complex"


def test_unsupported_degree():
    degree, result = solve("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
    assert degree == 3
    assert result["kind"] == "unsupported_degree"


def test_constant_on_right_side_without_x_power():
    degree, result = solve("1 * X^0 + 2 * X^1 + 5 * X^2 = 0")
    assert degree == 2
    assert result["kind"] == "two_complex"

def test_rhs_zero_literal_is_allowed():
    degree, result = solve("1 * X^0 + 2 * X^1 + 5 * X^2 = 0")
    assert degree == 2
    assert result["kind"] == "two_complex"

def test_constant_only_equation_is_rejected():
    with pytest.raises(ValueError):
        parse_equation("0 = 0")

    with pytest.raises(ValueError):
        parse_equation("1 = 1")