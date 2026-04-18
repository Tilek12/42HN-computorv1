import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMPUTOR = PROJECT_ROOT / "computor.py"


def run_cli(args: list[str], *, input_text: str | None = None, timeout: int = 8):
    proc = subprocess.run(
        [sys.executable, str(COMPUTOR), *args],
        input=input_text,
        text=True,
        capture_output=True,
        cwd=str(PROJECT_ROOT),
        timeout=timeout,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def test_cli_free_mode_basic():
    code, out = run_cli(["--free", "5 + 4 * X + X^2 = X^2"])
    assert code == 0
    assert "Polynomial degree: 1" in out
    assert "The solution is:" in out
    assert "-1.25" in out


def test_cli_strict_rejects_free_form_when_default_strict():
    code, out = run_cli(["X=5"])
    assert code == 1
    assert "Input error:" in out


def test_cli_steps_flag_shows_intermediate_values():
    code, out = run_cli(["--steps", "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"])
    assert code == 0
    assert "[steps] a=" in out
    assert "[steps] Δ = b² - 4ac =" in out


def test_cli_fraction_flag_linear():
    code, out = run_cli(["--fraction", "1 * X^0 + 4 * X^1 = 0"])
    assert code == 0
    assert "The solution is:" in out
    assert "-1/4" in out


def test_cli_fraction_flag_complex():
    code, out = run_cli(["--fraction", "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"])
    assert code == 0
    assert "two complex solutions" in out
    assert "-1/5 + 2/5i" in out
    assert "-1/5 - 2/5i" in out


def test_cli_precision_flag():
    code, out = run_cli(["--precision", "3", "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"])
    assert code == 0
    assert "0.905" in out
    assert "-0.475" in out


def test_cli_invalid_precision_low():
    code, out = run_cli(["--precision", "-1", "5 * X^0 + 4 * X^1 = 4 * X^0"])
    assert code == 1
    assert "Precision must be between 0 and 15" in out


def test_cli_invalid_precision_high():
    code, out = run_cli(["--precision", "42", "5 * X^0 + 4 * X^1 = 4 * X^0"])
    assert code == 1
    assert "Precision must be between 0 and 15" in out


def test_cli_unsupported_degree_in_free_mode():
    code, out = run_cli(["--free", "X^3 + 1 = 0"])
    assert code == 0
    assert "Polynomial degree: 3" in out
    assert "strictly greater than 2" in out


def test_cli_reads_from_stdin_when_no_equation_argument():
    code, out = run_cli([], input_text="5 * X^0 + 4 * X^1 = 4 * X^0\n")
    assert code == 0
    assert "Polynomial degree: 1" in out
    assert "The solution is:" in out


def test_cli_repl_mode_free():
    code, out = run_cli(
        ["--free", "--repl"],
        input_text="5 + 4*X + X^2 = X^2\nquit\n",
    )
    assert code == 0
    assert "Computor REPL mode" in out
    assert "Polynomial degree: 1" in out
    assert "The solution is:" in out


def test_cli_free_mode_error_message_invalid_operator():
    code, out = run_cli(["--free", "2 ** X^2 = 0"])
    assert code == 1
    assert "Input error:" in out