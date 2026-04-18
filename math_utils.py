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