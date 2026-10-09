from __future__ import annotations

import ast
import math
import operator
import re
from dataclasses import dataclass
from typing import Callable


class CalculatorError(ValueError):
    """Raised for invalid or unsafe calculator expressions."""


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
_TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d*)?|\.\d+)|([+\-*/%]))\s*")


def _validate_expression(expression: str) -> None:
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Enter an expression")
    position = 0
    expect_number = True
    saw_number = False
    while position < len(expression):
        match = _TOKEN.match(expression, position)
        if not match:
            raise CalculatorError("Invalid expression")
        number, symbol = match.groups()
        position = match.end()
        if number:
            if not expect_number:
                raise CalculatorError("Invalid expression")
            saw_number = True
            expect_number = False
        elif symbol:
            if expect_number:
                if saw_number or symbol not in "+-":
                    raise CalculatorError("Invalid expression")
            else:
                expect_number = True
    if not saw_number or expect_number:
        raise CalculatorError("Invalid expression")


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if (isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)):
        value = float(node.value)
        if math.isfinite(value):
            return value
        raise CalculatorError("Non-finite numbers are not supported")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        try:
            result = _BINARY_OPERATORS[type(node.op)](left, right)
        except (ZeroDivisionError, OverflowError) as exc:
            raise CalculatorError("Invalid arithmetic operation") from exc
        if not math.isfinite(result):
            raise CalculatorError("Result is not finite")
        return result
    raise CalculatorError("Unsupported expression")


def evaluate_expression(expression: str) -> float:
    _validate_expression(expression)
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError) as exc:
        raise CalculatorError("Invalid expression") from exc
    return _evaluate(tree)


def _format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return format(value, ".15g")


@dataclass
class CalculatorController:
    display: str = "0"
    _just_evaluated: bool = False

    def dispatch(self, action: str) -> str:
        if not isinstance(action, str):
            raise ValueError("Calculator action must be a string")
        if action == "clear":
            self.display = "0"
            self._just_evaluated = False
        elif action == "backspace":
            self.display = self.display[:-1] or "0"
            self._just_evaluated = False
        elif action == "sign":
            if self.display == "Error":
                self.display = "0"
            elif self.display != "0":
                self.display = (self.display[1:] if self.display.startswith("-")
                                else "-" + self.display)
            self._just_evaluated = False
        elif action == "=":
            try:
                self.display = _format_number(evaluate_expression(self.display))
            except CalculatorError:
                self.display = "Error"
            self._just_evaluated = True
        elif action in "0123456789.":
            if self.display == "Error" or self._just_evaluated:
                self.display = "0"
                self._just_evaluated = False
            if action == ".":
                current = re.split(r"[+\-*/%]", self.display)[-1]
                if "." in current:
                    return self.display
                if current == "":
                    self.display += "0"
            if self.display == "0" and action != ".":
                self.display = action
            else:
                self.display += action
        elif action in "+-*/%":
            if self.display == "Error":
                self.display = "0"
            self.display = re.sub(r"[+\-*/%]+$", "", self.display) + action
            self._just_evaluated = False
        else:
            raise ValueError(f"Unknown calculator action: {action!r}")
        return self.display


def handle_action(controller: CalculatorController, action: str) -> str:
    return controller.dispatch(action)
