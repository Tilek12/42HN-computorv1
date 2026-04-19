# Computor v1

A polynomial equation solver.  
Supports equations of degree `<= 2` (mandatory) with additional bonus features.

## Highlights

- Mandatory strict parser (`a * X^p`)
- Bonus free-form parser (examples: `2X^2-3X+1=0`, `X=5`)
- Reduced form output
- Degree detection
- Real and complex solutions
- Optional flags:
  - `--steps`
  - `--fraction`
  - `--precision`
  - `--repl`
  - `--strict` / `--free`

---

## Project structure

```text
computorv1/
├── computor.py           # CLI entrypoint
├── constants.py          # global constants (EPS, precision bounds, max degree)
├── shared_types.py       # shared type aliases (Term, Terms, Coeffs, ParsedEquation)
├── parser.py             # parser mode dispatcher
├── parser_strict.py      # mandatory parser
├── parser_free.py        # bonus free-form parser
├── reducer.py            # move RHS to LHS and combine powers
├── solver.py             # degree 0/1/2 solver
├── formatters.py         # reduced form + solution output
├── math_utils.py         # custom math helpers (sqrt, gcd, fraction)
├── docs/
│   └── knowledge.md      # math-only project knowledge base
└── tests/                # mandatory + bonus tests
    ├── test_mandatory_main.py
    ├── test_mandatory_plus.py
    ├── test_bonus_free.py
    └── test_bonus_cli.py
```

---

## Requirements

- Linux
- Python 3.10+
- `pytest` for tests

---

## Setup (Linux)

```bash
# Check Python
python3 --version

# (If needed) install Python tooling
sudo apt update
sudo apt install -y python3 python3-venv python3-pip

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install test dependency
python -m pip install --upgrade pip
python -m pip install pytest
```

---

## Test commands

```bash
# Run full suite
python -m pytest -q

# Verbose
python -m pytest -v

# Stop on first failure
python -m pytest -x

# One test file
python -m pytest -v tests/test_mandatory_main.py

# One test case
python -m pytest -v tests/test_bonus_free.py::test_free_accepts_subject_bonus_example
```

---

## Usage

## 1) Strict mode (default, mandatory-safe)

```bash
python computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
python computor.py --strict "5 * X^0 + 4 * X^1 = 4 * X^0"
```

## 2) Free mode (bonus)

```bash
python computor.py --free "5 + 4 * X + X^2 = X^2"
python computor.py --free "2X^2-3X+1=0"
python computor.py --free "X=5"
```

## 3) Extra flags

```bash
# Show intermediate values (a, b, c, Δ)
python computor.py --steps "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"

# Print results as irreducible fractions when possible
python computor.py --fraction "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"

# Control decimal precision
python computor.py --precision 3 "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"

# Combine flags
python computor.py --free --steps --fraction --precision 5 "2X^2-3X+1=0"
```

## 4) REPL mode

```bash
python computor.py --repl
python computor.py --free --repl
```

Type `exit` or `quit` to stop.

---

## Notes

- Keep mandatory evaluations in strict mode.
- Free-form parsing is bonus and enabled explicitly via `--free`.
- Mathematical explanations are kept in `docs/knowledge.md`.