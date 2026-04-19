from typing import TypeAlias

Term: TypeAlias = tuple[float, int]
Terms: TypeAlias = list[Term]
ParsedEquation: TypeAlias = tuple[Terms, Terms]

Coeffs: TypeAlias = dict[int, float]
ComplexPair: TypeAlias = tuple[float, float]