from math_utils import ft_abs, ft_sqrt, is_zero
from constants import MAX_SUPPORTED_DEGREE
from shared_types import Coeffs


def _solve_degree_zero(c: float) -> dict:
    return {"kind": "all_real"} if is_zero(c) else {"kind": "no_solution"}


def _solve_degree_one(b: float, c: float) -> dict:
    if is_zero(b):
        return _solve_degree_zero(c)
    return {"kind": "one_real", "x": -c / b}


def _solve_degree_two(a: float, b: float, c: float) -> dict:
    if is_zero(a):
        return _solve_degree_one(b, c)
    delta = b * b - 4.0 * a * c
    denom = 2.0 * a

    if is_zero(delta):
        return {"kind": "one_real_double", "delta": 0.0, "x": -b / denom}

    if delta > 0:
        sqrt_delta = ft_sqrt(delta)
        return {
            "kind": "two_real",
            "delta": delta,
            "x1": (-b - sqrt_delta) / denom,
            "x2": (-b + sqrt_delta) / denom,
        }

    real = -b / denom
    imag_abs = ft_sqrt(-delta) / ft_abs(denom)
    return {
        "kind": "two_complex",
        "delta": delta,
        "z1": (real, imag_abs),
        "z2": (real, -imag_abs),
    }


def solve_polynomial(coeffs: Coeffs, degree: int) -> dict:
    """Solve reduced polynomial according to computed degree."""
    c = coeffs.get(0, 0.0)
    b = coeffs.get(1, 0.0)
    a = coeffs.get(2, 0.0)

    if degree > MAX_SUPPORTED_DEGREE:
        return {"kind": "unsupported_degree"}
    if degree == 0:
        return _solve_degree_zero(c)
    if degree == 1:
        return _solve_degree_one(b, c)
    return _solve_degree_two(a, b, c)