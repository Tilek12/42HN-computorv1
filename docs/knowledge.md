# Computor v1 — Math Knowledge Base

## Purpose

This document contains the mathematical background used by Computor v1:

- polynomial normalization
- degree detection
- solving rules for degree 0 / 1 / 2
- discriminant logic
- precision considerations

---

## 1) Polynomial model

A polynomial equation is reduced to:

`a0 * X^0 + a1 * X^1 + ... + an * X^n = 0`

For Computor v1 (mandatory scope), we solve only:

- degree `0`
- degree `1`
- degree `2`

If degree `> 2`, it is reported as unsupported.

---

## 2) Term, coefficient, power

A term has the form:

`a * X^p`

Where:

- `a`: coefficient (real number)
- `p`: exponent/power (`p >= 0`, integer)
- `X`: unknown

Examples:

- `-9.3 * X^2` -> coefficient `-9.3`, power `2`
- `4 * X^0` -> constant term (`X^0 = 1`)

---

## 3) Reduction to canonical form

Given:

`L(X) = R(X)`

Move everything to the left:

`L(X) - R(X) = 0`

Then combine coefficients having the same power.

### Sign rule during move

- `+k * X^p` on RHS becomes `-k * X^p` on LHS
- `-k * X^p` on RHS becomes `+k * X^p` on LHS

---

## 4) Polynomial degree

Degree is the highest power with a non-zero coefficient.

Examples:

- `0*X^2 + 4*X^1 + 1*X^0 = 0` -> degree `1`
- `0*X^2 + 0*X^1 + 5*X^0 = 0` -> degree `0`
- all coefficients zero -> degree `0` (identity case)

---

## 5) Solving by degree

## Degree 0

Form: `c = 0`

- if `c = 0` -> infinitely many solutions (all real numbers)
- if `c != 0` -> no solution

---

## Degree 1

Form: `b * X + c = 0`

Solution (if `b != 0`):

`X = -c / b`

If `b = 0`, equation falls back to degree-0 logic.

---

## Degree 2

Form: `a * X^2 + b * X + c = 0` with `a != 0`

Discriminant:

`D = b^2 - 4ac`

### Cases

1. `D > 0` -> two real solutions

- `X1 = (-b - sqrt(D)) / (2a)`
- `X2 = (-b + sqrt(D)) / (2a)`

2. `D = 0` -> one double real solution

- `X = -b / (2a)`

3. `D < 0` -> two complex conjugate solutions

- `X = -b / (2a) ± i * sqrt(-D) / (2a)`

---

## 6) Complex numbers (minimum needed)

Complex number format:

`u + v*i`, where `i^2 = -1`

In this project, complex values appear only when `D < 0`.

---

## 7) Precision and epsilon

Floating-point arithmetic may introduce tiny residual errors.

Use epsilon comparison:

- treat value as zero when `abs(value) < eps` (for example `1e-12`)

This impacts:

- degree detection
- discriminant classification
- reduced-form cleanup

---

## 8) Reference edge cases

1. `6 * X^0 = 6 * X^0`  
   Reduced: `0 * X^0 = 0` -> all real numbers.

2. `10 * X^0 = 15 * X^0`  
   Reduced: `-5 * X^0 = 0` -> no solution.

3. Non-zero `X^3` term present  
   Degree `3` -> unsupported in mandatory solver.

---

## 9) Mental model

Pipeline:

`parse -> reduce -> combine -> degree -> solve`

This is the core mathematical workflow of Computor v1.