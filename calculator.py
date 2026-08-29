def calculator():
    print("Simple Calculator")
    print("-----------------")
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")
    
    while True:
        try:
            # Get operation choice
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '5':
                print("Goodbye!")
                break
            
            if choice not in ['1', '2', '3', '4']:
                print("Invalid input. Please enter 1-5.")
                continue
            
            # Get numbers
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            # Perform operation
            if choice == '1':
                result = num1 + num2
                print(f"{num1} + {num2} = {result}")
            elif choice == '2':
                result = num1 - num2
                print(f"{num1} - {num2} = {result}")
            elif choice == '3':
                result = num1 * num2
                print(f"{num1} × {num2} = {result}")
            elif choice == '4':
                if num2 == 0:
                    print("Error: Division by zero is not allowed!")
                else:
                    result = num1 / num2
                    print(f"{num1} ÷ {num2} = {result}")
        
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    calculator()
