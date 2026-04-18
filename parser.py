from parser_strict import parse_equation_strict
from parser_free import parse_equation_free

Term = tuple[float, int]


def parse_equation(equation: str, mode: str = "strict") -> tuple[list[Term], list[Term]]:
    if mode == "strict":
        return parse_equation_strict(equation)
    if mode == "free":
        return parse_equation_free(equation)
    raise ValueError(f"Unknown parser mode: '{mode}'")