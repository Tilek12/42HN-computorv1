import sys
from parser import parse_equation


def main() -> int:
    # If argument exists, use it. Otherwise read from stdin.
    if len(sys.argv) > 1:
        equation = sys.argv[1]
    else:
        equation = input("Enter equation: ").strip()

    try:
        lhs_terms, rhs_terms = parse_equation(equation)

        print("Parsed successfully.")
        print("LHS terms:", lhs_terms)
        print("RHS terms:", rhs_terms)
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())