from math_utils import ft_abs, ft_sqrt, is_zero


def _solve_degree_zero(c: float) -> dict:
    if is_zero(c):
        return {"kind": "all_real"}
    return {"kind": "no_solution"}


def _solve_degree_one(b: float, c: float) -> dict:
    if is_zero(b):
        return {"kind": "no_solution"}
    return {"kind": "one_real", "x": -c / b}


def _solve_degree_two(a: float, b: float, c: float) -> dict:
    delta = b * b - 4.0 * a * c

    if is_zero(delta):
        return {"kind": "one_real_double", "delta": 0.0, "x": -b / (2.0 * a)}

    if delta > 0:
        sqrt_delta = ft_sqrt(delta)
        denom = 2.0 * a
        return {
            "kind": "two_real",
            "delta": delta,
            "x1": (-b - sqrt_delta) / denom,
            "x2": (-b + sqrt_delta) / denom,
        }

    # delta < 0: complex roots
    denom = 2.0 * a
    real = -b / denom
    imag_abs = ft_sqrt(-delta) / ft_abs(denom)
    return {
        "kind": "two_complex",
        "delta": delta,
        "z1": (real, imag_abs),
        "z2": (real, -imag_abs),
    }


def solve_polynomial(coeffs: dict[int, float], degree: int) -> dict:
    """Solve reduced polynomial according to computed degree."""
    c = coeffs.get(0, 0.0)
    b = coeffs.get(1, 0.0)
    a = coeffs.get(2, 0.0)

    if degree > 2:
        return {"kind": "unsupported_degree"}
    if degree == 0:
        return _solve_degree_zero(c)
    if degree == 1:
        return _solve_degree_one(b, c)
    return _solve_degree_two(a, b, c)