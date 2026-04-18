import re

Term = tuple[float, int]

NUM_RE = re.compile(r"^\d+(?:\.\d+)?$")
ALLOWED_CHARS_RE = re.compile(r"^[0-9Xx+\-*/^.\s=]+$")


def _compact(text: str) -> str:
    return "".join(text.split())


def _split_terms(compact_side: str) -> list[str]:
    terms: list[str] = []
    start = 0
    for i, ch in enumerate(compact_side):
        if i > 0 and ch in "+-" and compact_side[i - 1] != "^":
            terms.append(compact_side[start:i])
            start = i
    terms.append(compact_side[start:])
    return terms


def _validate_chars(text: str) -> None:
    if not ALLOWED_CHARS_RE.match(text):
        raise ValueError("Invalid character in expression")


def _parse_token(token: str) -> Term:
    """
    Supported forms (free mode):
    - 5
    - X
    - -X
    - 3X
    - 3*X
    - X^2
    - 3X^2
    - 3*X^2
    """
    if not token:
        raise ValueError("Invalid syntax: empty term")

    sign = 1.0
    body = token
    if token[0] in "+-":
        sign = -1.0 if token[0] == "-" else 1.0
        body = token[1:]

    if not body:
        raise ValueError("Invalid syntax: dangling sign")

    if "x" in body:
        raise ValueError("Invalid variable: use uppercase 'X'")

    if "X" not in body:
        if "*" in body or "^" in body or "/" in body:
            raise ValueError(f"Invalid constant token: '{token}'")
        if not NUM_RE.match(body):
            raise ValueError(f"Invalid constant token: '{token}'")
        return sign * float(body), 0

    if body.count("X") != 1:
        raise ValueError(f"Invalid term token: '{token}'")

    left, right = body.split("X", 1)

    # Coefficient before X
    if left == "":
        coeff = 1.0
    else:
        if left.endswith("*"):
            left = left[:-1]
        if not left or not NUM_RE.match(left):
            raise ValueError(f"Invalid coefficient in token: '{token}'")
        coeff = float(left)

    # Exponent after X
    if right == "":
        power = 1
    else:
        if not right.startswith("^"):
            raise ValueError(f"Invalid exponent syntax in token: '{token}'")
        exp_str = right[1:]
        if not exp_str:
            raise ValueError(f"Missing exponent in token: '{token}'")
        if exp_str.startswith("-"):
            raise ValueError(f"Negative exponents are not supported: '{token}'")
        if "." in exp_str or not exp_str.isdigit():
            raise ValueError(f"Exponent must be a non-negative integer: '{token}'")
        power = int(exp_str)

    return sign * coeff, power


def parse_side_free(side: str) -> list[Term]:
    compact_side = _compact(side)

    if not compact_side:
        raise ValueError("Invalid side: empty expression")
    if "=" in compact_side:
        raise ValueError("Invalid syntax: unexpected '=' inside side")
    if compact_side[0] == "+":
        raise ValueError("Invalid syntax: leading '+' operator")
    if compact_side[-1] in "+-":
        raise ValueError("Invalid syntax: trailing operator")
    if "**" in compact_side or "//" in compact_side:
        raise ValueError("Invalid operator sequence in expression")

    tokens = _split_terms(compact_side)
    return [_parse_token(tok) for tok in tokens]


def parse_equation_free(equation: str) -> tuple[list[Term], list[Term]]:
    if not equation or not equation.strip():
        raise ValueError("Equation must not be empty")
    _validate_chars(equation)
    if equation.count("=") != 1:
        raise ValueError("Equation must contain exactly one '='")

    left, right = equation.split("=", 1)
    if not left.strip():
        raise ValueError("Left side is empty")
    if not right.strip():
        raise ValueError("Right side is empty")

    lhs_terms = parse_side_free(left)
    rhs_terms = parse_side_free(right)
    return lhs_terms, rhs_terms