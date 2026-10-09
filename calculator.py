import ast
import operator
import sys

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str):
    """Safely evaluate a basic arithmetic expression."""
    expression = expression.strip()
    if not expression:
        raise ValueError("expression cannot be empty")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("exponent is too large")
            return _OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("only numeric arithmetic is allowed")

    try:
        return evaluate(ast.parse(expression, mode="eval"))
    except ZeroDivisionError:
        raise ValueError("division by zero") from None
    except (SyntaxError, TypeError, OverflowError):
        raise ValueError("invalid arithmetic expression") from None


def main():
    expression = " ".join(sys.argv[1:])
    if expression:
        try:
            print(calculate(expression))
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        return 0

    print("Calculator (type 'quit' to exit)")
    while True:
        try:
            expression = input("> ")
        except EOFError:
            print()
            break
        if expression.strip().lower() in {"quit", "exit"}:
            break
        try:
            print(calculate(expression))
        except ValueError as error:
            print(f"Error: {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
