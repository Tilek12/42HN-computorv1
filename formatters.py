from math_utils import ft_abs, is_zero, ft_fraction_str


def format_number(value: float, precision: int = 6) -> str:
    """Format a float for human-readable output."""
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.{precision}f}".rstrip("0").rstrip(".")


def _format_fraction(value: float) -> str:
    return ft_fraction_str(value)

def _highest_non_zero_power(coeffs: dict[int, float]) -> int:
    powers = [p for p, c in coeffs.items() if not is_zero(c)]
    return max(powers) if powers else 0


def format_reduced_form(coeffs: dict[int, float]) -> str:
    if not coeffs:
        return "0 * X^0 = 0"

    max_power = _highest_non_zero_power(coeffs)
    if max_power == 0 and is_zero(coeffs.get(0, 0.0)):
        return "0 * X^0 = 0"

    parts: list[str] = []
    for power in range(0, max_power + 1):
        coeff = coeffs.get(power, 0.0)
        term = f"{format_number(ft_abs(coeff))} * X^{power}"
        if not parts:
            parts.append(f"-{term}" if coeff < 0 else term)
        else:
            parts.append(f"{'-' if coeff < 0 else '+'} {term}")
    return " ".join(parts) + " = 0"


def format_solution(result: dict, *, precision: int = 6, fraction: bool = False) -> str:
    kind = result["kind"]

    if kind == "unsupported_degree":
        return "The polynomial degree is strictly greater than 2, I can't solve."
    if kind == "all_real":
        return "Any real number is a solution."
    if kind == "no_solution":
        return "No solution."

    if kind == "one_real":
        x = _format_fraction(result["x"]) if fraction else format_number(result["x"], precision)
        return f"The solution is:\n{x}"

    if kind == "one_real_double":
        x = _format_fraction(result["x"]) if fraction else format_number(result["x"], precision)
        return f"Discriminant is equal to zero, the solution is:\n{x}"

    if kind == "two_real":
        x1 = _format_fraction(result["x1"]) if fraction else format_number(result["x1"], precision)
        x2 = _format_fraction(result["x2"]) if fraction else format_number(result["x2"], precision)
        return f"Discriminant is strictly positive, the two solutions are:\n{x1}\n{x2}"

    if kind == "two_complex":
        r1, i1 = result["z1"]
        r2, i2 = result["z2"]

        if fraction:
            r1s = _format_fraction(r1)
            r2s = _format_fraction(r2)
            i1s = _format_fraction(ft_abs(i1))
            i2s = _format_fraction(ft_abs(i2))
        else:
            r1s = format_number(r1, precision)
            r2s = format_number(r2, precision)
            i1s = format_number(ft_abs(i1), precision)
            i2s = format_number(ft_abs(i2), precision)

        s1 = "-" if i1 < 0 else "+"
        s2 = "-" if i2 < 0 else "+"
        return (
            "Discriminant is strictly negative, the two complex solutions are:\n"
            f"{r1s} {s1} {i1s}i\n"
            f"{r2s} {s2} {i2s}i"
        )

    return "Unknown solver state."