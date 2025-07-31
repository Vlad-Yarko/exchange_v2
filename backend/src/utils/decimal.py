def format_decimal(number: float, decimal_places: int = 3) -> float:
    formatted_number = f"{number:.{decimal_places}f}"
    return float(formatted_number)
