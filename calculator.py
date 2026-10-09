from __future__ import annotations

import ast
import operator
from decimal import Decimal, InvalidOperation


class CalculatorError(ValueError):
    """Raised when an expression cannot be safely evaluated."""


class SafeEvaluator(ast.NodeVisitor):
    _binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def evaluate(self, expression: str) -> Decimal:
        if not isinstance(expression, str) or not expression.strip():
            raise CalculatorError("Expression is empty")
        try:
            tree = ast.parse(expression, mode="eval")
        except (SyntaxError, ValueError) as exc:
            raise CalculatorError("Malformed expression") from exc
        return self.visit(tree.body)

    def visit_Constant(self, node: ast.Constant) -> Decimal:
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError("Unsupported value")
        try:
            return Decimal(str(node.value))
        except InvalidOperation as exc:
            raise CalculatorError("Invalid number") from exc

    def visit_BinOp(self, node: ast.BinOp) -> Decimal:
        operation = self._binary_ops.get(type(node.op))
        if operation is None:
            raise CalculatorError("Unsupported operator")
        left, right = self.visit(node.left), self.visit(node.right)
        if isinstance(node.op, ast.Pow) and right != right.to_integral_value():
            raise CalculatorError("Exponent must be an integer")
        try:
            return operation(left, right)
        except (ArithmeticError, InvalidOperation, ZeroDivisionError) as exc:
            raise CalculatorError("Invalid arithmetic operation") from exc

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Decimal:
        operation = self._unary_ops.get(type(node.op))
        if operation is None:
            raise CalculatorError("Unsupported operator")
        return operation(self.visit(node.operand))

    def generic_visit(self, node: ast.AST) -> Decimal:
        raise CalculatorError("Unsupported syntax")


def evaluate(expression: str) -> Decimal:
    return SafeEvaluator().evaluate(expression)


def format_result(value: Decimal) -> str:
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


# Focused engine smoke tests.
assert evaluate("2 + 3 * 4") == Decimal("14")
assert evaluate("-2 + +3") == Decimal("1")
assert evaluate("0.10 + 0.20") == Decimal("0.30")
assert format_result(Decimal("10.5000")) == "10.5"
assert format_result(Decimal("0")) == "0"

for expression in ("", "2 +", "foo", "2 // 3", "[1, 2]", "1 / 0"):
    try:
        evaluate(expression)
    except CalculatorError:
        pass
    else:
        raise AssertionError(f"accepted invalid expression: {expression!r}")

print("engine tests passed")