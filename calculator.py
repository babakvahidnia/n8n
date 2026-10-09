import ast
import operator

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def evaluate(expression: str):
    """Safely evaluate a basic numeric arithmetic expression."""
    if not expression or not expression.strip():
        raise ValueError("expression cannot be empty")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("invalid expression") from exc
    return _evaluate_node(tree.body)


def _evaluate_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        return _BINARY_OPERATORS[type(node.op)](_evaluate_node(node.left), _evaluate_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand))
    raise ValueError("only numeric arithmetic is supported")


assert evaluate("2 * (3 + 4) - 1") == 13
assert evaluate("-2 ** 2") == -4
assert evaluate("7 // 2") == 3
try:
    evaluate("__import__('os').system('echo unsafe')")
except ValueError:
    pass
else:
    raise AssertionError("unsafe expression was accepted")
print("calculator tests passed")