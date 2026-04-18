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
    return coeffs, degree, result


# --------------------------
# Valid + edge behavior
# --------------------------

def test_many_spaces_should_parse():
    coeffs, degree, result = solve("  5  *  X^0   +  4 * X^1   =   4 * X^0 ")
    assert degree == 1
    assert result["kind"] == "one_real"
    assert ft_abs(result["x"] + 0.25) < 1e-9


def test_duplicate_powers_are_combined():
    coeffs, degree, result = solve("1 * X^1 + 2 * X^1 + 3 * X^0 = 0")
    assert coeffs[1] == 3.0
    assert coeffs[0] == 3.0
    assert degree == 1
    assert result["kind"] == "one_real"
    assert ft_abs(result["x"] + 1.0) < 1e-9


def test_terms_cancel_to_zero_identity():
    coeffs, degree, result = solve("2 * X^2 - 2 * X^2 + 5 * X^0 = 5 * X^0")
    assert degree == 0
    assert result["kind"] == "all_real"


def test_zero_high_degree_should_not_raise_degree():
    coeffs, degree, result = solve("0 * X^3 + 1 * X^1 = 0")
    assert degree == 1
    assert result["kind"] == "one_real"
    assert ft_abs(result["x"]) < 1e-12


def test_constant_only_true():
    coeffs, degree, result = solve("3 = 3")
    assert degree == 0
    assert result["kind"] == "all_real"


def test_constant_only_false():
    coeffs, degree, result = solve("3 = 4")
    assert degree == 0
    assert result["kind"] == "no_solution"


def test_linear_zero_solution():
    coeffs, degree, result = solve("2 * X^1 = 0")
    assert degree == 1
    assert result["kind"] == "one_real"
    assert ft_abs(result["x"]) < 1e-12


def test_quadratic_delta_positive():
    coeffs, degree, result = solve("1 * X^2 - 3 * X^1 + 2 * X^0 = 0")
    assert degree == 2
    assert result["kind"] == "two_real"
    roots = sorted([result["x1"], result["x2"]])
    assert ft_abs(roots[0] - 1.0) < 1e-9
    assert ft_abs(roots[1] - 2.0) < 1e-9


def test_quadratic_delta_zero():
    coeffs, degree, result = solve("1 * X^2 + 2 * X^1 + 1 * X^0 = 0")
    assert degree == 2
    assert result["kind"] == "one_real_double"
    assert ft_abs(result["x"] + 1.0) < 1e-9


def test_quadratic_delta_negative():
    coeffs, degree, result = solve("1 * X^2 + 0 * X^1 + 1 * X^0 = 0")
    assert degree == 2
    assert result["kind"] == "two_complex"
    (r1, i1), (r2, i2) = result["z1"], result["z2"]
    assert ft_abs(r1) < 1e-9 and ft_abs(r2) < 1e-9
    assert ft_abs(ft_abs(i1) - 1.0) < 1e-9
    assert ft_abs(ft_abs(i2) - 1.0) < 1e-9


def test_negative_a_complex_branch_signs():
    coeffs, degree, result = solve("-1 * X^2 + 0 * X^1 - 1 * X^0 = 0")
    assert degree == 2
    assert result["kind"] == "two_complex"
    (r1, i1), (r2, i2) = result["z1"], result["z2"]
    assert ft_abs(r1) < 1e-9 and ft_abs(r2) < 1e-9
    assert i1 < 0 < i2


def test_unsupported_degree_4():
    coeffs, degree, result = solve("1 * X^4 + 1 * X^1 = 0")
    assert degree == 4
    assert result["kind"] == "unsupported_degree"


def test_epsilon_cleanup_degree_zero():
    # should collapse to 0 with epsilon normalization in reducer
    coeffs, degree, result = solve("0.0000000000001 * X^1 = 0")
    assert degree == 0


# --------------------------
# Invalid / wrong input
# --------------------------

def test_invalid_missing_equal():
    with pytest.raises(ValueError):
        parse_equation("1 * X^1 + 2 * X^0")


def test_invalid_empty_input():
    with pytest.raises(ValueError):
        parse_equation("")


def test_invalid_term_missing_power():
    with pytest.raises(ValueError):
        parse_equation("2 * X = 0")


def test_invalid_lowercase_x():
    with pytest.raises(ValueError):
        parse_equation("2 * x^1 = 0")


def test_invalid_negative_exponent():
    with pytest.raises(ValueError):
        parse_equation("2 * X^-1 = 0")


def test_invalid_float_exponent():
    with pytest.raises(ValueError):
        parse_equation("2 * X^1.5 = 0")


def test_invalid_missing_coefficient():
    with pytest.raises(ValueError):
        parse_equation("* X^2 = 0")


def test_invalid_bad_operator():
    with pytest.raises(ValueError):
        parse_equation("2 ** X^2 = 0")


def test_invalid_trailing_plus():
    with pytest.raises(ValueError):
        parse_equation("2 * X^1 + = 0")


def test_invalid_multiple_equal():
    with pytest.raises(ValueError):
        parse_equation("1 * X^1 = 2 * X^0 = 3 * X^0")


def test_invalid_empty_left_side():
    with pytest.raises(ValueError):
        parse_equation("= 0")


def test_invalid_empty_right_side():
    with pytest.raises(ValueError):
        parse_equation("1 * X^0 =")


def test_invalid_leading_plus():
    with pytest.raises(ValueError):
        parse_equation("+ 2 * X^1 = 0")


def test_invalid_repeated_plus():
    with pytest.raises(ValueError):
        parse_equation("1 * X^1 ++ 2 * X^0 = 0")