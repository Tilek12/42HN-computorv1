import re

# Mandatory format term: a * X^p
# Examples matched:
#   5 * X^0
#   -9.3 * X^2
TERM_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)\*X\^(\d+)$")


def _split_terms(side: str) -> list[str]:
    """
    Convert:
      '5 * X^0 + 4 * X^1 - 9.3 * X^2'
    into:
      ['5 * X^0', '4 * X^1', '-9.3 * X^2']
    """
    # Turn '-' into '+-' then split on '+'
    normalized = side.strip().replace("-", "+-")
    parts = [p.strip() for p in normalized.split("+") if p.strip()]
    return parts


def parse_side(side: str) -> list[tuple[float, int]]:
    terms: list[tuple[float, int]] = []

    for raw_term in _split_terms(side):
        compact_term = raw_term.replace(" ", "") # Remove all spaces for regex matching
        match = TERM_RE.match(compact_term)
        if not match:
            raise ValueError(f"Invalid term format: '{raw_term}'")

        coefficient = float(match.group(1))
        power = int(match.group(2))
        terms.append((coefficient, power))

    return terms


def parse_equation(equation: str) -> tuple[list[tuple[float, int]], list[tuple[float, int]]]:
    if "=" not in equation:
        raise ValueError("Equation must contain '='")

    left, right = equation.split("=", 1)
    lhs_terms = parse_side(left)
    rhs_terms = parse_side(right)
    return lhs_terms, rhs_terms