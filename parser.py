from parser_strict import parse_equation_strict
from parser_free import parse_equation_free
from shared_types import ParsedEquation


def parse_equation(equation: str, mode: str = "strict") -> ParsedEquation:
    if mode == "strict":
        return parse_equation_strict(equation)
    if mode == "free":
        return parse_equation_free(equation)
    raise ValueError(f"Unknown parser mode: '{mode}'")