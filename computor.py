import sys
from parser import parse_equation
from reducer import reduce_terms, polynomial_degree
from formatters import format_reduced_form


def main() -> int:
    # If argument exists, use it. Otherwise read from stdin.
    if len(sys.argv) > 1:
        equation = sys.argv[1]
    else:
        equation = input("Enter equation: ").strip()

    try:
        lhs_terms, rhs_terms = parse_equation(equation)
        coeffs = reduce_terms(lhs_terms, rhs_terms)
        degree = polynomial_degree(coeffs)

        print("Parsed successfully.")
        print("LHS terms:", lhs_terms)
        print("RHS terms:", rhs_terms)
        print("Reduced coefficients:", coeffs)
        print("Polynomial degree:", degree)

        print(f"Reduced form: {format_reduced_form(coeffs)}")
        print(f"Polynomial degree: {degree}")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())