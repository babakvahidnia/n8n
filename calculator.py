# Simple console-based calculator with basic arithmetic operations.
# The program presents a menu, accepts user input, performs the chosen operation,
# and displays the result. It continues until the user chooses to exit.

def calculator():
    """Run a simple interactive calculator in the terminal.

    Presents a menu of operations and repeatedly prompts the user to
    choose an operation and enter two numbers, until the user chooses
    to exit.
    """
    # Display the calculator header and available operations
    print("Simple Calculator")
    print("-----------------")
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")
    
    # Main input loop: keep asking the user until they choose to exit
    while True:
        try:
            # Get operation choice from the user as a string
            choice = input("\nEnter your choice (1-5): ")
            
            # If the user chooses '5', exit the calculator
            if choice == '5':
                print("Goodbye!")
                break
            
            # Validate the operation choice; prompt again if invalid
            if choice not in ['1', '2', '3', '4']:
                print("Invalid input. Please enter 1-5.")
                continue
            
            # Prompt user for the first operand and convert to float
            num1 = float(input("Enter first number: "))
            # Prompt user for the second operand and convert to float
            num2 = float(input("Enter second number: "))
            
            # Perform the selected operation and display the result
            if choice == '1':
                # Addition
                result = num1 + num2
                print(f"{num1} + {num2} = {result}")
            elif choice == '2':
                # Subtraction
                result = num1 - num2
                print(f"{num1} - {num2} = {result}")
            elif choice == '3':
                # Multiplication
                result = num1 * num2
                print(f"{num1} × {num2} = {result}")
            elif choice == '4':
                # Division with zero-division guard
                if num2 == 0:
                    # Handle division by zero error
                    print("Error: Division by zero is not allowed!")
                else:
                    # Perform division
                    result = num1 / num2
                    print(f"{num1} ÷ {num2} = {result}")
        
        # Handle cases where number conversion fails (invalid numeric input)
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

# Run the calculator only if this script is executed directly
if __name__ == "__main__":
    calculator()