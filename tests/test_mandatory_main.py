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


def test_subject_example_1_two_real():
    # "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
    degree, result = solve("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    assert degree == 2
    assert result["kind"] == "two_real"
    assert ft_abs(result["x1"] - 0.905239) < 1e-6
    assert ft_abs(result["x2"] + 0.475131) < 1e-6


def test_subject_example_2_degree_1():
    # "5 * X^0 + 4 * X^1 = 4 * X^0"
    degree, result = solve("5 * X^0 + 4 * X^1 = 4 * X^0")
    assert degree == 1
    assert result["kind"] == "one_real"
    assert ft_abs(result["x"] + 0.25) < 1e-9


def test_subject_example_3_unsupported_degree():
    # "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
    degree, result = solve("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
    assert degree == 3
    assert result["kind"] == "unsupported_degree"


def test_subject_example_4_all_real():
    # "6 * X^0 = 6 * X^0"
    degree, result = solve("6 * X^0 = 6 * X^0")
    assert degree == 0
    assert result["kind"] == "all_real"


def test_subject_example_5_no_solution():
    # "10 * X^0 = 15 * X^0"
    degree, result = solve("10 * X^0 = 15 * X^0")
    assert degree == 0
    assert result["kind"] == "no_solution"


def test_subject_example_6_two_complex_rhs_zero_literal():
    # "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
    degree, result = solve("1 * X^0 + 2 * X^1 + 5 * X^2 = 0")
    assert degree == 2
    assert result["kind"] == "two_complex"

    (r1, i1), (r2, i2) = result["z1"], result["z2"]
    assert ft_abs(r1 + 0.2) < 1e-9
    assert ft_abs(r2 + 0.2) < 1e-9
    assert ft_abs(ft_abs(i1) - 0.4) < 1e-9
    assert ft_abs(ft_abs(i2) - 0.4) < 1e-9


def test_mandatory_rejects_constant_only_equations():
    with pytest.raises(ValueError):
        parse_equation("0 = 0")
    with pytest.raises(ValueError):
        parse_equation("1 = 1")