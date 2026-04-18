EPS = 1e-12


def is_zero(value: float, eps: float = EPS) -> bool:
    return -eps < value < eps


def ft_abs(value: float) -> float:
    return -value if value < 0 else value


def ft_sqrt(value: float, eps: float = EPS, max_iter: int = 10_000) -> float:
    """Newton-Raphson square root without math library."""
    if value < 0:
        raise ValueError("Cannot sqrt negative number in real domain.")
    if is_zero(value, eps):
        return 0.0

    x = value if value >= 1.0 else 1.0
    for _ in range(max_iter):
        nx = 0.5 * (x + value / x)
        if ft_abs(nx - x) < eps:
            return nx
        x = nx

    raise RuntimeError("ft_sqrt did not converge")


def ft_gcd(a: int, b: int) -> int:
    """Greatest common divisor (Euclidean algorithm)."""
    a = -a if a < 0 else a
    b = -b if b < 0 else b
    while b:
        a, b = b, a % b
    return a if a != 0 else 1


def ft_to_fraction(value: float, precision: int = 12) -> tuple[int, int]:
    """
    Convert float to reduced fraction using rounded decimal representation.
    """
    if is_zero(value):
        return 0, 1

    if precision < 0:
        precision = 0
    if precision > 15:
        precision = 15

    sign = -1 if value < 0 else 1
    abs_value = -value if value < 0 else value

    s = f"{abs_value:.{precision}f}"
    if "." not in s:
        return sign * int(s), 1

    int_part, frac_part = s.split(".", 1)
    frac_part = frac_part.rstrip("0")
    if not frac_part:
        return sign * int(int_part), 1

    den = 10 ** len(frac_part)
    num = int(int_part) * den + int(frac_part)
    num *= sign

    g = ft_gcd(num, den)
    return num // g, den // g


def ft_fraction_str(value: float, precision: int = 12) -> str:
    """Render float as irreducible fraction string."""
    num, den = ft_to_fraction(value, precision=precision)
    if den == 1:
        return str(num)
    return f"{num}/{den}"