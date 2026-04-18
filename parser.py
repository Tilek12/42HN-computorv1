import re

# Mandatory format term: a * X^p
# Examples matched:
#   5 * X^0
#   -9.3 * X^2
TERM_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)\*X\^(\d+)$")
CONST_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)$")


def _validate_side_syntax(side: str) -> None:
    s = side.replace(" ", "")
    if not s:
        raise ValueError("Invalid side: empty expression")
    
    # Invalid endings like: "2*X^1+" or "2*X^1-"
    if s[-1] in "+-":
        raise ValueError("Invalid syntax: trailing operator")
    
    # Invalid starts like: "+2*X^1"
    if s[0] == "+":
        raise ValueError("Invalid syntax: leading '+' operator")
    
    # Reject repeated operators
    invalid_pairs = ("++", "--", "+-", "-+")
    if any(pair in s for pair in invalid_pairs):
        raise ValueError("Invalid syntax: repeated operators")


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
    _validate_side_syntax(side)

    terms: list[tuple[float, int]] = []

    for raw_term in _split_terms(side):
        compact_term = raw_term.replace(" ", "") # Remove all spaces for regex matching
        
        # 1. a*X^p
        match = TERM_RE.match(compact_term)
        if match:
            coefficient = float(match.group(1))
            power = int(match.group(2))
            terms.append((coefficient, power))
            continue

        # 2. contsant number => X^0
        const_match = CONST_RE.match(compact_term)
        if const_match:
            coefficient = float(const_match.group(1))
            power = 0
            terms.append((coefficient, power))
            continue

        raise ValueError(f"Invalid term format: '{raw_term}'")
    
    return terms


def parse_equation(equation: str) -> tuple[list[tuple[float, int]], list[tuple[float, int]]]:
    if "=" not in equation:
        raise ValueError("Equation must contain '='")

    left, right = equation.split("=", 1)
    lhs_terms = parse_side(left)
    rhs_terms = parse_side(right)
    return lhs_terms, rhs_terms