def solve_polynomial(coeffs: dict[int, float], degree: int) -> dict:
    """
    Step version:
    - handles degree 0 and 1
    - keeps placeholders for degree 2 and >2
    """
    c = coeffs.get(0, 0.0)
    b = coeffs.get(1, 0.0)

    if degree > 2:
        return {"kind": "unsupported_degree"}
    
    if degree == 0:
        if c == 0:
            return {"kind": "all_real"}
        return {"kind": "no_solution"}
    
    if degree == 1:
        x = -c / b
        return {"kind": "one_real", "x": x}
    
    # Degree == 2 (next step)
    return {"kind": "degree_2_pending"}
