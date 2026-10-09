import ast
import operator
import sys


class CalculatorError(Exception):
    """Expected, user-facing calculator error."""


class SafeEvaluator(ast.NodeVisitor):
    _binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return float(node.value)
        raise CalculatorError("Invalid number")

    def visit_BinOp(self, node):
        operation = self._binary_operators.get(type(node.op))
        if operation is None:
            raise CalculatorError("Unsupported operator")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise CalculatorError("Cannot divide by zero")
        return operation(left, right)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            return -self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return self.visit(node.operand)
        raise CalculatorError("Unsupported operator")

    def generic_visit(self, node):
        raise CalculatorError("Invalid expression")


def evaluate(expression):
    try:
        tree = ast.parse(expression, mode="eval")
        return SafeEvaluator().visit(tree)
    except CalculatorError:
        raise
    except (SyntaxError, ValueError, OverflowError):
        raise CalculatorError("Incomplete or invalid expression") from None


def format_result(value):
    return "0" if value == 0 else f"{value:.12g}"


class CalculatorApp:
    def __init__(self, root, tk, ttk):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.expression = tk.StringVar()
        self.just_calculated = False
        self.display = ttk.Entry(
            root, textvariable=self.expression, justify="right",
            font=("TkDefaultFont", 20), state="readonly", width=18,
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 6), ipady=8)
        self._create_buttons(ttk)
        root.bind("<Key>", self._on_key)

    def _create_buttons(self, ttk):
        buttons = [
            ("C", 1, 0, self.clear), ("⌫", 1, 1, self.backspace),
            ("÷", 1, 2, lambda: self.add_operator("/")),
            ("×", 1, 3, lambda: self.add_operator("*")),
            ("7", 2, 0, lambda: self.add_digit("7")),
            ("8", 2, 1, lambda: self.add_digit("8")),
            ("9", 2, 2, lambda: self.add_digit("9")),
            ("-", 2, 3, lambda: self.add_operator("-")),
            ("4", 3, 0, lambda: self.add_digit("4")),
            ("5", 3, 1, lambda: self.add_digit("5")),
            ("6", 3, 2, lambda: self.add_digit("6")),
            ("+", 3, 3, lambda: self.add_operator("+")),
            ("1", 4, 0, lambda: self.add_digit("1")),
            ("2", 4, 1, lambda: self.add_digit("2")),
            ("3", 4, 2, lambda: self.add_digit("3")),
            ("=", 4, 3, self.calculate), ("0", 5, 0, lambda: self.add_digit("0")),
            (".", 5, 1, self.add_decimal),
        ]
        for label, row, column, command in buttons:
            ttk.Button(self.root, text=label, command=command, width=5).grid(
                row=row, column=column, padx=3, pady=3, ipady=6
            )

    def _reset_after_result(self):
        if self.just_calculated:
            self.expression.set("")
            self.just_calculated = False

    def add_digit(self, digit):
        self._reset_after_result()
        self.expression.set(self.expression.get() + digit)

    def add_decimal(self):
        self._reset_after_result()
        text = self.expression.get()
        current = text
        for symbol in "+-*/":
            current = current.rsplit(symbol, 1)[-1]
        if "." not in current:
            prefix = "0" if not text or text[-1] in "+-*/" else ""
            self.expression.set(text + prefix + ".")

    def add_operator(self, symbol):
        self.just_calculated = False
        text = self.expression.get()
        if not text:
            if symbol == "-":
                self.expression.set("-")
            return
        self.expression.set(text[:-1] + symbol if text[-1] in "+-*/" else text + symbol)

    def clear(self):
        self.expression.set("")
        self.just_calculated = False

    def backspace(self):
        self.just_calculated = False
        self.expression.set(self.expression.get()[:-1])

    def calculate(self):
        text = self.expression.get()
        if not text:
            return
        try:
            self.expression.set(format_result(evaluate(text)))
        except CalculatorError as error:
            self.expression.set(f"Error: {error}")
        self.just_calculated = True

    def _on_key(self, event):
        if event.char in "0123456789":
            self.add_digit(event.char)
        elif event.char == ".":
            self.add_decimal()
        elif event.char in "+-*/":
            self.add_operator(event.char)
        elif event.keysym in ("Return", "equal"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()


def main():
    try:
        import tkinter as tk
        from tkinter import ttk
        root = tk.Tk()
    except ImportError as error:
        print(f"Tkinter is required to run the graphical calculator: {error}", file=sys.stderr)
        return
    except (OSError, tk.TclError) as error:
        print(f"Unable to start the graphical calculator: {error}", file=sys.stderr)
        return

    CalculatorApp(root, tk, ttk)
    root.mainloop()


# Logic tests run without requiring a display or Tk libraries.
assert evaluate("2 + 3 * 4") == 14.0
assert evaluate("-2.5 + 5") == 2.5
assert format_result(evaluate("10 / 4")) == "2.5"
try:
    evaluate("1 / 0")
except CalculatorError as error:
    assert str(error) == "Cannot divide by zero"
else:
    raise AssertionError("division by zero was not rejected")


if __name__ == "__main__":
    main()
