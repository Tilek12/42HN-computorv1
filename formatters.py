from math_utils import ft_abs, is_zero


def format_number(value: float) -> str:
    """Format a float for human-readable output."""
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _highest_non_zero_power(coeffs: dict[int, float]) -> int:
    """Return highest non-zero power, or 0 if polynomial is null."""
    powers = [p for p, c in coeffs.items() if not is_zero(c)]
    return max(powers) if powers else 0


def format_reduced_form(coeffs: dict[int, float]) -> str:
    """
    Build the reduced form from X^0 to highest non-zero degree.
    Keep intermediate missing powers as 0 * X^p.
    """
    if not coeffs:
        return "0 * X^0 = 0"

    max_power = _highest_non_zero_power(coeffs)
    if max_power == 0 and is_zero(coeffs.get(0, 0.0)):
        return "0 * X^0 = 0"

    parts: list[str] = []

    for power in range(0, max_power + 1):
        coeff = coeffs.get(power, 0.0)
        abs_coeff = ft_abs(coeff)
        term = f"{format_number(abs_coeff)} * X^{power}"

        if not parts:
            parts.append(f"-{term}" if coeff < 0 else term)
        else:
            parts.append(f"{'-' if coeff < 0 else '+'} {term}")

    return " ".join(parts) + " = 0"


def format_solution(result: dict) -> str:
    """Format solver result dictionary into final user-facing text."""
    kind = result["kind"]

    if kind == "unsupported_degree":
        return "The polynomial degree is strictly greater than 2, I can't solve."

    if kind == "all_real":
        return "Any real number is a solution."

    if kind == "no_solution":
        return "No solution."

    if kind == "one_real":
        return f"The solution is:\n{format_number(result['x'])}"

    if kind == "one_real_double":
        return f"Discriminant is equal to zero, the solution is:\n{format_number(result['x'])}"

    if kind == "two_real":
        return (
            "Discriminant is strictly positive, the two solutions are:\n"
            f"{format_number(result['x1'])}\n"
            f"{format_number(result['x2'])}"
        )

    if kind == "two_complex":
        r1, i1 = result["z1"]
        r2, i2 = result["z2"]
        s1 = "-" if i1 < 0 else "+"
        s2 = "-" if i2 < 0 else "+"
        return (
            "Discriminant is strictly negative, the two complex solutions are:\n"
            f"{format_number(r1)} {s1} {format_number(ft_abs(i1))}i\n"
            f"{format_number(r2)} {s2} {format_number(ft_abs(i2))}i"
        )

    return "Unknown solver state."