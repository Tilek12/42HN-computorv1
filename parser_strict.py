import re
from shared_types import ParsedEquation, Terms


TERM_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)\*X\^(\d+)$")
CONST_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)$")


def _compact(text: str) -> str:
    return "".join(text.split())


def _split_terms(compact_side: str) -> list[str]:
    """Split by top-level + and -, keeping sign on each token."""
    terms: list[str] = []
    start = 0
    for i, ch in enumerate(compact_side):
        if i > 0 and ch in "+-":
            terms.append(compact_side[start:i])
            start = i
    terms.append(compact_side[start:])
    return terms


def _validate_side_syntax(compact_side: str) -> None:
    if not compact_side:
        raise ValueError("Invalid side: empty expression")
    if "=" in compact_side:
        raise ValueError("Invalid syntax: unexpected '=' inside side")
    if compact_side[0] == "+":
        raise ValueError("Invalid syntax: leading '+' operator")
    if compact_side[-1] in "+-":
        raise ValueError("Invalid syntax: trailing operator")

    for bad in ("++", "--", "+-", "-+"):
        if bad in compact_side:
            raise ValueError("Invalid syntax: repeated operators")


def parse_side_strict(side: str, *, allow_zero_literal: bool) -> Terms:
    """Parse one side in mandatory strict mode (a*X^p only)."""
    compact_side = _compact(side)
    _validate_side_syntax(compact_side)

    tokens = _split_terms(compact_side)
    terms: Terms = []

    for token in tokens:
        m = TERM_RE.match(token)
        if m:
            coeff = float(m.group(1))
            power = int(m.group(2))
            terms.append((coeff, power))
            continue

        cm = CONST_RE.match(token)
        if cm:
            value = float(cm.group(1))
            if allow_zero_literal and len(tokens) == 1 and value == 0.0:
                terms.append((0.0, 0))
                continue

        raise ValueError(
            f"Invalid term format: '{token}'.\n"
            "Mandatory format is a*X^p (example: 5 * X^0 - 3.2 * X^2).\n"
            "Only standalone zero is accepted on right side: '= 0'."
        )

    return terms


def parse_equation_strict(equation: str) -> ParsedEquation:
    if not equation or not equation.strip():
        raise ValueError("Equation must not be empty")
    if equation.count("=") != 1:
        raise ValueError("Equation must contain exactly one '='")

    compact_eq = _compact(equation)
    if "X" not in compact_eq:
        raise ValueError(
            "Mandatory mode requires at least one polynomial term with X "
            "(e.g. '1 * X^1 = 0')."
        )

    left, right = equation.split("=", 1)
    if not left.strip():
        raise ValueError("Left side is empty")
    if not right.strip():
        raise ValueError("Right side is empty")

    lhs_terms = parse_side_strict(left, allow_zero_literal=False)
    rhs_terms = parse_side_strict(right, allow_zero_literal=True)
    return lhs_terms, rhs_terms