def get_number(prompt, input_func=input, output_func=print):
    """Read a valid floating-point number from the user."""
    while True:
        try:
            return float(input_func(prompt))
        except ValueError:
            output_func("Please enter a valid number.")
        except EOFError:
            raise


def calculate(choice, first, second):
    """Return (result, operator), or raise ZeroDivisionError for division by zero."""
    operations = {
        "1": (first + second, "+"),
        "2": (first - second, "-"),
        "3": (first * second, "*"),
    }
    if choice in operations:
        return operations[choice]
    if choice == "4":
        if second == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return first / second, "/"
    raise ValueError("Invalid calculator choice.")


def main(input_func=input, output_func=print):
    while True:
        output_func("\nCalculator Menu")
        output_func("1. Addition")
        output_func("2. Subtraction")
        output_func("3. Multiplication")
        output_func("4. Division")
        output_func("5. Exit")

        try:
            choice = input_func("Choose an option (1-5): ").strip()
        except EOFError:
            output_func("\nInput ended. Goodbye!")
            break

        if choice == "5":
            output_func("Goodbye!")
            break

        if choice not in {"1", "2", "3", "4"}:
            output_func("Invalid choice. Please select an option from 1 to 5.")
            continue

        try:
            first = get_number("Enter the first number: ", input_func, output_func)
            second = get_number("Enter the second number: ", input_func, output_func)
            result, operation = calculate(choice, first, second)
        except EOFError:
            output_func("\nInput ended. Goodbye!")
            break
        except ZeroDivisionError:
            output_func("Cannot divide by zero.")
            continue

        output_func(f"Result: {first} {operation} {second} = {result}")


if __name__ == "__main__":
    main()
