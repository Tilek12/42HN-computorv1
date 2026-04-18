import re

# Mandatory strict term: a*X^p
TERM_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)\*X\^(\d+)$")
CONST_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)$")


def _compact(text: str) -> str:
    return text.replace(" ", "")


def _split_terms(compact_side: str) -> list[str]:
    """
    Split by + / - while keeping sign with each term.
    Example:
      '5*X^0+4*X^1-9.3*X^2' -> ['5*X^0', '+4*X^1', '-9.3*X^2']
    """
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

    # Reject repeated operators in middle (++, --, +-, -+)
    for bad in ("++", "--", "+-", "-+"):
        if bad in compact_side:
            raise ValueError("Invalid syntax: repeated operators")


def parse_side(side: str, *, allow_zero_literal: bool) -> list[tuple[float, int]]:
    compact_side = _compact(side)
    _validate_side_syntax(compact_side)

    tokens = _split_terms(compact_side)
    terms: list[tuple[float, int]] = []

    for token in tokens:
        m = TERM_RE.match(token)
        if m:
            coeff = float(m.group(1))
            power = int(m.group(2))
            terms.append((coeff, power))
            continue

        # Mandatory exception used in subject examples: "... = 0"
        cm = CONST_RE.match(token)
        if cm:
            value = float(cm.group(1))
            if allow_zero_literal and len(tokens) == 1 and value == 0.0:
                terms.append((0.0, 0))
                continue

        raise ValueError(
            f"Invalid term format: '{token}'. \n"
            "Mandatory format is a*X^p (example: 5 * X^0 - 3.2 * X^2). \n"
            "Only standalone zero is accepted on right side: '= 0'."
        )

    return terms


def parse_equation(equation: str) -> tuple[list[tuple[float, int]], list[tuple[float, int]]]:
    if not equation or not equation.strip():
        raise ValueError("Equation must not be empty")
    if equation.count("=") != 1:
        raise ValueError("Equation must contain exactly one '='")

    compact_eq = _compact(equation)

    # Mandatory guard: reject constant-only equations like 0=0, 1=1
    if "X" not in compact_eq:
        raise ValueError(
            "Mandatory mode requires at least one polynomial term with X "
            "(e.g. '1 * X^1 = 0')."
        )

    left, right = equation.split("=")
    if not left.strip():
        raise ValueError("Left side is empty")
    if not right.strip():
        raise ValueError("Right side is empty")

    lhs_terms = parse_side(left, allow_zero_literal=False)
    rhs_terms = parse_side(right, allow_zero_literal=True)
    return lhs_terms, rhs_terms
