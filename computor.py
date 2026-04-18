import sys
from parser import parse_equation
from reducer import reduce_terms, polynomial_degree
from formatters import format_reduced_form, format_solution
from solver import solve_polynomial


def main() -> int:
    try:
        # If argument exists, use it. Otherwise read from stdin.
        if len(sys.argv) > 1:
            equation = sys.argv[1]
        else:
            equation = input("Enter equation: ").strip()
    except KeyboardInterrupt:
        print("\nInput cancelled.")
        return 130
    except EOFError:
        print("\nNo input provided.")
        return 0

    try:
        lhs_terms, rhs_terms = parse_equation(equation)
        coeffs = reduce_terms(lhs_terms, rhs_terms)
        degree = polynomial_degree(coeffs)

        print(f"Reduced form: {format_reduced_form(coeffs)}")
        print(f"Polynomial degree: {degree}")

        result = solve_polynomial(coeffs, degree)
        print(format_solution(result))

        return 0

    except ValueError as ve:
        print(f"Input error: {ve}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())