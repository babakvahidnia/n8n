"""A small command-line calculator."""

from __future__ import annotations


def calculate(left: float, operator: str, right: float) -> float:
    """Apply an arithmetic operator to two numbers."""
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("cannot divide by zero")
        return left / right
    raise ValueError(f"unsupported operator: {operator}")


def main() -> None:
    """Read a simple expression and print its result."""
    print("Calculator (enter q to quit)")

    while True:
        try:
            expression = input("> ").strip()
        except EOFError:
            print()
            break

        if expression.lower() in {"q", "quit", "exit"}:
            break

        parts = expression.split()
        if len(parts) != 3:
            print("Use the format: number operator number")
            continue

        try:
            left, operator, right = float(parts[0]), parts[1], float(parts[2])
            print(calculate(left, operator, right))
        except (ValueError, ZeroDivisionError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
