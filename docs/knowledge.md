# Computor v1 — Knowledge Base

## 1. Project overview

Computor v1 is a polynomial equation solver for degree 2 or lower.

The program:
1. Reads an equation
2. Reduces it to `... = 0`
3. Detects polynomial degree
4. Solves the equation based on the degree
5. Prints the solution(s), including complex solutions for degree 2 when needed

---

## 2. Input format (mandatory part)

Each term is written like:

`a * X^p`

Where:
- `a` = coefficient (can be integer, decimal, negative, or zero)
- `X` = variable
- `p` = exponent (power)

Example:

`5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0`

---

## 3. Terminology

- **Term**: one part like `-9.3 * X^2`
- **Coefficient**: numeric value before `X^p` (`-9.3`)
- **Exponent / power**: value after `^` (`2`)
- **Reduced form**: all terms moved to left side, right side becomes `0`
- **Polynomial degree**: highest exponent with non-zero coefficient

---

## 4. Reduction to standard form

The equation is transformed to:

`a * X^2 + b * X^1 + c * X^0 = 0`

General process:
- Move all right-side terms to the left
- Change their sign
- Combine terms with the same exponent

Example:

Input:
`5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0`

Reduced:
`4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0`

---

## 5. Degree detection

Degree is the highest exponent with coefficient not equal to zero.

Examples:
- `0 * X^2 + 4 * X^1 + 1 * X^0 = 0` -> degree `1`
- `0 * X^2 + 0 * X^1 + 5 * X^0 = 0` -> degree `0`
- `0 * X^2 + 0 * X^1 + 0 * X^0 = 0` -> special case (`0 = 0`)
- any non-zero `X^3` term -> degree `3` (not solved in mandatory part)

---

## 6. Solving by degree

## Degree 0

Form:
`c = 0`

Cases:
- `c = 0` -> infinitely many solutions (all real numbers)
- `c != 0` -> no solution

---

## Degree 1

Form:
`b * X + c = 0`

Solution:
`X = -c / b`

Example:
`1 + 4X = 0` -> `X = -1/4 = -0.25`

---

## Degree 2

Form:
`a * X^2 + b * X + c = 0`

Discriminant:
`D = b^2 - 4ac`

Cases:

1. `D > 0`  
   Two real solutions:
   - `X1 = (-b - sqrt(D)) / (2a)`
   - `X2 = (-b + sqrt(D)) / (2a)`

2. `D = 0`  
   One real double solution:
   - `X = -b / (2a)`

3. `D < 0`  
   Two complex solutions:
   - `X1 = (-b / (2a)) - i * sqrt(-D) / (2a)`
   - `X2 = (-b / (2a)) + i * sqrt(-D) / (2a)`

---

## 7. Complex numbers (minimum needed)

Complex form:
`u + vi`

Where:
- `u` = real part
- `v` = imaginary coefficient
- `i^2 = -1`

Used only when discriminant is negative.

Example:
`1 * X^2 + 2 * X + 5 = 0`
- `D = 4 - 20 = -16`
- `X = -1 +/- 2i`

---

## 8. Important edge cases

1. Same both sides:
   - `6 * X^0 = 6 * X^0`
   - Reduced: `0 * X^0 = 0`
   - Result: all real numbers

2. Contradiction:
   - `10 * X^0 = 15 * X^0`
   - Reduced: `-5 * X^0 = 0`
   - Result: no solution

3. Degree greater than 2:
   - cannot solve in mandatory part

4. Zero coefficients:
   - valid and kept during reduction
   - ignored for degree if coefficient is zero

---

## 9. Sign handling during reduction

When moving a term from right to left, sign changes:

- `+k * X^p` on right -> `-k * X^p` on left
- `-k * X^p` on right -> `+k * X^p` on left

This is critical for correct coefficients.

---

## 10. Precision notes

Floating-point arithmetic can produce tiny errors, like `0.000000000001`.

Common handling:
- use small epsilon (example: `1e-12`)
- treat values with `abs(value) < epsilon` as zero

This helps with:
- degree detection
- discriminant classification (`D > 0`, `D = 0`, `D < 0`)

---

## 11. Quick examples

### Example A — degree 1
`5 * X^0 + 4 * X^1 = 4 * X^0`  
Reduced: `1 * X^0 + 4 * X^1 = 0`  
Solution: `X = -0.25`

### Example B — degree 2, positive discriminant
`4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0`  
`D > 0` -> two real solutions

### Example C — degree 2, negative discriminant
`1 * X^0 + 2 * X^1 + 5 * X^2 = 0`  
`D = -16` -> two complex solutions: `-1/5 +/- 2i/5`

### Example D — identity
`0 = 0` -> all real numbers are solutions

### Example E — impossible equation
`-5 = 0` -> no solution

---

## 12. Mental model

Computor v1 follows one clean pipeline:

`parse -> reduce -> combine -> detect degree -> solve -> print result`

This model explains the full mandatory part clearly during peer evaluation.
