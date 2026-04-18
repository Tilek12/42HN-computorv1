def format_number(value: float) -> str:
    # Show integers without .0
    if value.is_integer():
        return str(int(value))
    #keep a clean decimal representation
    return f"{value:.6f}".rstrip("0").rstrip(".")


def format_reduced_form(coeffs: dict[int, float]) -> str:
    if not coeffs:
        return "0 * X^0 = 0"
    
    max_power = max(coeffs.keys())
    parts: list[str] = []

    for power in range(0, max_power + 1):
        coeff = coeffs.get(power, 0.0)
        abs_coeff = abs(coeff)
        term = f"{format_number(abs_coeff)} * X^{power}"

        if not parts:
            #first term keeps sign directly
            if coeff < 0:
                parts.append(f"- {term}")
            else:
                parts.append(term)
        else:
            sign = "-" if coeff < 0 else "+"
            parts.append(f"{sign} {term}")

    return " ".join(parts) + " = 0"
