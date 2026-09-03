# ماشین‌حساب ساده مبتنی بر کنسول با عملیات حسابی پایه.
# این برنامه یک منو ارائه می‌کند، ورودی کاربر را می‌پذیرد، عملیات انتخاب‌شده را انجام می‌دهد
# و نتیجه را نمایش می‌دهد. تا زمانی که کاربر خروج را انتخاب کند، به کار خود ادامه می‌دهد.

def calculator():
    """Run a simple interactive calculator in the terminal.

    Presents a menu of operations and repeatedly prompts the user to
    choose an operation and enter two numbers, until the user chooses
    to exit.
    """
    # نمایش سربرگ ماشین‌حساب و عملیات‌های در دسترس
    print("Simple Calculator")
    print("-----------------")
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)" )
    print("5. Exit")
    
    # حلقه ورودی اصلی: تا زمانی که کاربر خروج را انتخاب کند، از کاربر درخواست ورودی می‌گیرد
    while True:
        try:
            # دریافت انتخاب عملیات از کاربر به صورت رشته
            choice = input("\nEnter your choice (1-5): ")
            
            # اگر کاربر گزینه '5' را انتخاب کند، ماشین حساب را خارج کنید
            if choice == '5':
                print("Goodbye!")
                break
            
            # اعتبارسنجی انتخاب عملیات؛ در صورت نامعتبر بودن دوباره از کاربر درخواست کنید
            if choice not in ['1', '2', '3', '4']:
                print("Invalid input. Please enter 1-5.")
                continue
            
            # کاربر را برای ورود عدد اول ورودی هدایت کنید و به مقدار اعشاری تبدیل کنید
            num1 = float(input("Enter first number: "))
            # کاربر را برای ورود عدد دوم ورودی هدایت کنید و به مقدار اعشاری تبدیل کنید
            num2 = float(input("Enter second number: "))
            
            # انجام عملیات انتخاب‌شده و نمایش نتیجه
            if choice == '1':
                # جمع
                result = num1 + num2
                print(f"{num1} + {num2} = {result}")
            elif choice == '2':
                # تفریق
                result = num1 - num2
                print(f"{num1} - {num2} = {result}")
            elif choice == '3':
                # ضرب
                result = num1 * num2
                print(f"{num1} × {num2} = {result}")
            elif choice == '4':
                # تقسیم با بررسی تقسیم بر صفر
                if num2 == 0:
                    # مدیریت خطای تقسیم بر صفر
                    print("Error: Division by zero is not allowed!")
                else:
                    # انجام تقسیم
                    result = num1 / num2
                    print(f"{num1} ÷ {num2} = {result}")
        
        # مدیریت مواردی که تبدیل عددی ناموفق است (ورودی عددی نامعتبر)
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

# اجرای ماشین حساب تنها در صورتی که این اسکریپت مستقیماً اجرا شود
if __name__ == "__main__":
    calculator()
