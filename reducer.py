from math_utils import is_zero
from shared_types import Coeffs, Terms


def reduce_terms(
    lhs_terms: Terms,
    rhs_terms: Terms,
) -> Coeffs:
    """
    Reduce equation to left side only: lhs - rhs = 0.
    Returns coefficients indexed by polynomial power.
    """
    coeffs: Coeffs = {}

    for coeff, power in lhs_terms:
        coeffs[power] = coeffs.get(power, 0.0) + coeff

    for coeff, power in rhs_terms:
        coeffs[power] = coeffs.get(power, 0.0) - coeff

    for power in list(coeffs.keys()):
        if is_zero(coeffs[power]):
            coeffs[power] = 0.0

    return coeffs


def polynomial_degree(coeffs: Coeffs) -> int:
    """Degree = highest power with non-zero coefficient, else 0."""
    non_zero_powers = [p for p, c in coeffs.items() if not is_zero(c)]
    return max(non_zero_powers) if non_zero_powers else 0