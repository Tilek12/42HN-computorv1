def reduce_terms(
    lhs_terms: list[tuple[float, int]],
    rhs_terms: list[tuple[float, int]],
) -> dict[int, float]:
    """
    Returns coefficients map by power after reduction to left side:
    lhs - rhs = 0

    Example:
        lhs: [(5,0), (4,1), (-9.3,2)]
        rhs: [(1,0)]
        result: {0: 4, 1: 4, 2: -9.3}
    """
    coeffs: dict[int, float] = {}

    # Add left side terms
    for coeff, power in lhs_terms:
        coeffs[power] = coeffs.get(power, 0.0) + coeff

    # Subtract right side terms
    for coeff, power in rhs_terms:
        coeffs[power] = coeffs.get(power, 0.0) - coeff

    return coeffs


def polynomial_degree(coeffs: dict[int, float]) -> int:
    """
    Degree = highest power with non-zero coefficient.
    If all are zero, return 0.
    """
    non_zero_powers = [p for p, c in coeffs.items() if c != 0]
    if not non_zero_powers:
        return 0
    return max(non_zero_powers)
