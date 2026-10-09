from __future__ import annotations

import ast
import math
import operator
from dataclasses import dataclass
from typing import Callable


class CalculatorError(ValueError):
    """Raised when an expression is invalid or unsafe."""


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    ):
        value = float(node.value)
        if not math.isfinite(value):
            raise CalculatorError("Non-finite numbers are not supported")
        return value

    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise CalculatorError("Exponent is too large")
        try:
            result = _BINARY_OPERATORS[type(node.op)](left, right)
        except (ZeroDivisionError, OverflowError) as exc:
            raise CalculatorError("Invalid arithmetic operation") from exc
        if not math.isfinite(result):
            raise CalculatorError("Result is not finite")
        return result

    raise CalculatorError("Unsupported expression")


def evaluate_expression(expression: str) -> float:
    """Evaluate only supported numeric arithmetic; never calls unrestricted eval."""
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Enter an expression")
    if len(expression) > 200:
        raise CalculatorError("Expression is too long")
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError) as exc:
        raise CalculatorError("Invalid expression") from exc
    return _evaluate(tree)


def _format_number(value: float) -> str:
    return str(int(value)) if value.is_integer() else format(value, ".15g")


@dataclass
class CalculatorController:
    """UI-agnostic controller. Bind calculator button callbacks to dispatch()."""

    display: str = "0"
    _just_evaluated: bool = False

    def dispatch(self, action: str) -> str:
        """Handle digits, operators, decimal, clear, backspace, sign, and equals."""
        if action == "clear":
            self.display, self._just_evaluated = "0", False
        elif action == "backspace":
            self.display = self.display[:-1] or "0"
            self._just_evaluated = False
        elif action == "sign":
            if self.display == "Error":
                self.display = "0"
            self.display = (
                "-" + self.display
                if not self.display.startswith("-")
                else self.display[1:]
            )
            self._just_evaluated = False
        elif action == "=":
            try:
                self.display = _format_number(evaluate_expression(self.display))
            except CalculatorError:
                self.display = "Error"
            self._just_evaluated = True
        elif action in "0123456789.":
            if self.display == "Error" or self._just_evaluated:
                self.display, self._just_evaluated = "0", False
            if action == ".":
                current_number = (
                    self.display.split("+")[-1]
                    .split("-")[-1]
                    .split("*")[-1]
                    .split("/")[-1]
                    .split("%")[-1]
                )
                if "." in current_number:
                    return self.display
            self.display = (
                action
                if self.display == "0" and action != "."
                else self.display + action
            )
        elif action in "+-*/%":
            if self.display == "Error":
                self.display = "0"
            self.display = self.display.rstrip("+-*/% ") + action
            self._just_evaluated = False
        else:
            raise ValueError(f"Unknown calculator action: {action!r}")
        return self.display


def handle_action(controller: CalculatorController, action: str) -> str:
    """Convenience adapter for existing UI callbacks."""
    return controller.dispatch(action)
