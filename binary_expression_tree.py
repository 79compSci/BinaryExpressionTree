"""Linked positional binary expression tree constructed from postfix tokens."""
import math
from stack import Stack


class BinaryExpressionTree:
    OPERATORS = {"+", "-", "*", "/"}

    class _Node:
        def __init__(self, element, parent=None, left=None, right=None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right

    class Position:
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            self._container._validate(self)
            return self._node.element

    def __init__(self, postfix=None):
        self._root = None
        self._size = 0
        if postfix is not None:
            built = self.from_postfix(postfix)
            self._root, self._size = built._root, built._size
            built._root, built._size = None, 0

    def __len__(self):
        return self._size

    def _make_position(self, node):
        return self.Position(self, node) if node is not None else None

    def _validate(self, p):
        if not isinstance(p, self.Position) or p._container is not self:
            raise ValueError("Position does not belong to this tree")
        node = p._node
        if node is None:
            raise ValueError("Invalid position")
        current = node
        while current.parent is not None:
            current = current.parent
        if current is not self._root:
            raise ValueError("Position is no longer owned by this tree")
        return node

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        return self._make_position(self._validate(p).parent)

    def left(self, p):
        return self._make_position(self._validate(p).left)

    def right(self, p):
        return self._make_position(self._validate(p).right)

    def _add_root(self, element):
        if self._root is not None:
            raise ValueError("Root already exists")
        self._root = self._Node(element)
        self._size = 1
        return self.root()

    def attach_subtrees(self, left_tree, right_tree):
        """Transfer exclusive ownership of two nonempty trees to this root.

        Source trees become empty, so transferred nodes cannot belong to
        two trees. Positions held from source trees become invalid.
        """
        if self._root is None or self._root.left or self._root.right:
            raise ValueError("Target must contain only an unattached root")
        if self._size != 1:
            raise ValueError("Target must contain exactly one node")
        if (left_tree is right_tree or self is left_tree or self is right_tree
                or not isinstance(left_tree, BinaryExpressionTree)
                or not isinstance(right_tree, BinaryExpressionTree)
                or left_tree._root is None or right_tree._root is None):
            raise ValueError("Two distinct nonempty source trees required")
        self._root.left = left_tree._root
        self._root.right = right_tree._root
        self._root.left.parent = self._root
        self._root.right.parent = self._root
        self._size += left_tree._size + right_tree._size
        left_tree._root, left_tree._size = None, 0
        right_tree._root, right_tree._size = None, 0

    @classmethod
    def from_postfix(cls, expression):
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Empty postfix expression")
        partial = Stack()
        for token in expression.split():
            if token in cls.OPERATORS:
                if partial.size() < 2:
                    raise ValueError("Too few operands")
                right_tree = partial.pop()
                left_tree = partial.pop()
                combined = cls()
                combined._add_root(token)
                combined.attach_subtrees(left_tree, right_tree)
                partial.push(combined)
            else:
                try:
                    value = float(token)
                except ValueError as exc:
                    raise ValueError(f"Unsupported token: {token}") from exc
                if not math.isfinite(value):
                    raise ValueError(f"Unsupported token: {token}")
                leaf = cls()
                leaf._add_root(token)
                partial.push(leaf)
        if partial.size() != 1:
            raise ValueError("Extra operands")
        return partial.pop()

    def _require_root(self):
        if self._root is None:
            raise ValueError("Empty expression tree")
        return self.root()

    def preorder(self):
        def visit(p):
            yield p
            for child in (self.left(p), self.right(p)):
                if child is not None:
                    yield from visit(child)
        yield from visit(self._require_root())

    def inorder(self):
        def visit(p):
            left = self.left(p)
            right = self.right(p)
            if left is not None:
                yield from visit(left)
            yield p
            if right is not None:
                yield from visit(right)
        yield from visit(self._require_root())

    def postorder(self):
        def visit(p):
            for child in (self.left(p), self.right(p)):
                if child is not None:
                    yield from visit(child)
            yield p
        yield from visit(self._require_root())

    def to_infix(self):
        def visit(p):
            left = self.left(p)
            if left is None:
                return p.element()
            return f"({visit(left)} {p.element()} {visit(self.right(p))})"
        return visit(self._require_root())

    def to_postfix(self):
        return " ".join(p.element() for p in self.postorder())

    def evaluate(self):
        def visit(p):
            left = self.left(p)
            if left is None:
                return float(p.element())
            a = visit(left)
            b = visit(self.right(p))
            op = p.element()
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        return visit(self._require_root())
