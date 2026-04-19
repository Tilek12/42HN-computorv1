import argparse

from parser import parse_equation
from reducer import reduce_terms, polynomial_degree
from formatters import format_reduced_form, format_solution
from solver import solve_polynomial


def _build_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Computor v1 polynomial solver")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true", help="Use mandatory strict parser (default)")
    mode.add_argument("--free", action="store_true", help="Use bonus free-form parser")

    parser.add_argument("--steps", action="store_true", help="Show intermediate steps")
    parser.add_argument("--fraction", action="store_true", help="Show solutions as irreducible fractions")
    parser.add_argument("--precision", type=int, default=6, help="Decimal precision for float output")
    parser.add_argument("--repl", action="store_true", help="Interactive mode")
    parser.add_argument("equation", nargs="?", help='Equation string, e.g. "5 * X^0 + 4 * X^1 = 4 * X^0"')
    return parser.parse_args()


def _validate_precision(precision: int) -> None:
    if precision < 0 or precision > 15:
        raise ValueError("Precision must be between 0 and 15")


def _print_steps(coeffs: dict[int, float], degree: int) -> None:
    a = coeffs.get(2, 0.0)
    b = coeffs.get(1, 0.0)
    c = coeffs.get(0, 0.0)
    print(f"[steps] a = {a}, b = {b}, c = {c}")
    if degree == 2:
        delta = b * b - 4.0 * a * c
        print(f"[steps] Δ = b² - 4ac = {delta}")


def _solve_once(equation: str, parser_mode: str, *, steps: bool, precision: int, fraction: bool) -> int:
    lhs_terms, rhs_terms = parse_equation(equation, mode=parser_mode)
    coeffs = reduce_terms(lhs_terms, rhs_terms)
    degree = polynomial_degree(coeffs)

    print(f"Reduced form: {format_reduced_form(coeffs, precision=precision, style=parser_mode)}")
    print(f"Polynomial degree: {degree}")

    result = solve_polynomial(coeffs, degree)

    if steps and degree <= 2:
        _print_steps(coeffs, degree)

    print(format_solution(result, precision=precision, fraction=fraction))
    return 0


def _run_repl(parser_mode: str, *, steps: bool, precision: int, fraction: bool) -> int:
    print("Computor REPL mode. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            equation = input("computor> ").strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 130

        if not equation:
            continue
        if equation.lower() in {"exit", "quit"}:
            return 0

        try:
            _solve_once(
                equation,
                parser_mode,
                steps=steps,
                precision=precision,
                fraction=fraction,
            )
        except ValueError as err:
            print(f"Input error: {err}")
        except Exception as err:
            print(f"Error: {err}")


def main() -> int:
    args = _build_args()
    parser_mode = "free" if args.free else "strict"

    try:
        _validate_precision(args.precision)

        if args.repl:
            if args.equation:
                _solve_once(
                    args.equation,
                    parser_mode,
                    steps=args.steps,
                    precision=args.precision,
                    fraction=args.fraction,
                )
            return _run_repl(
                parser_mode,
                steps=args.steps,
                precision=args.precision,
                fraction=args.fraction,
            )

        equation = args.equation
        if equation is None:
            equation = input("Enter equation: ").strip()

        return _solve_once(
            equation,
            parser_mode,
            steps=args.steps,
            precision=args.precision,
            fraction=args.fraction,
        )

    except KeyboardInterrupt:
        print("\nInput cancelled.")
        return 130
    except EOFError:
        print("\nNo input provided.")
        return 0
    except ValueError as err:
        print(f"Input error: {err}")
        return 1
    except Exception as err:
        print(f"Error: {err}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())