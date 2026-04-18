from math_utils import ft_abs, is_zero, ft_sqrt


def solve_polynomial(coeffs: dict[int, float], degree: int) -> dict:
    c = coeffs.get(0, 0.0)
    b = coeffs.get(1, 0.0)
    a = coeffs.get(2, 0.0)

    if degree > 2:
        return {"kind": "unsupported_degree"}
    
    if degree == 0:
        if is_zero(c):
            return {"kind": "all_real"}
        return {"kind": "no_solution"}
    
    if degree == 1:
        if is_zero(b):
            return {"kind": "no_solution"}
        x = -c / b
        return {"kind": "one_real", "x": x}
    
    # degree == 2
    delta = b * b - 4.0 * a * c

    if is_zero(delta):
        x = -b / (2.0 * a)
        return {"kind": "one_real_double", "delta": 0.0, "x": x}
    
    if delta > 0:
        sqrt_delta = ft_sqrt(delta)
        x1 = (-b - sqrt_delta) / (2.0 * a)
        x2 = (-b + sqrt_delta) / (2.0 * a)
        return {"kind": "two_real", "delta": delta, "x1": x1, "x2": x2}
    
    # delta < 0 -> complex roots
    denom = 2.0 * a
    real = -b / denom
    imag_abs = ft_sqrt(-delta) / ft_abs(denom)
    return {
        "kind": "two_complex",
        "delta": delta,
        "z1": (real, imag_abs),
        "z2": (real, -imag_abs)
    }
