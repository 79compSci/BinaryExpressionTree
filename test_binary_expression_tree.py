"""CSC 223 expression tree tests."""
import unittest
from binary_expression_tree import BinaryExpressionTree

class TestExpressionTree(unittest.TestCase):
    def build(self, s):
        return BinaryExpressionTree.from_postfix(s)

    def test_add(self):
        self.assertAlmostEqual(self.build("5 3 +").evaluate(), 8)

    def test_nested(self):
        t = self.build("5 3 8 * +")
        self.assertEqual(t.to_infix(), "(5 + (3 * 8))")
        self.assertAlmostEqual(t.evaluate(), 29)

    def test_order(self):
        self.assertAlmostEqual(self.build("8 2 / 3 -").evaluate(), 1)

    def test_negative_decimal(self):
        self.assertAlmostEqual(self.build("-2.5 4 *").evaluate(), -10)

    def test_too_few(self):
        with self.assertRaises(ValueError):
            self.build("5 +")

    def test_extra(self):
        with self.assertRaises(ValueError):
            self.build("5 3 2 +")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.build("8 0 /").evaluate()

    def test_round_trip(self):
        s = "5 3 8 * +"
        self.assertEqual(self.build(s).to_postfix(), s)

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.build(" ")

    def test_unsupported(self):
        with self.assertRaises(ValueError):
            self.build("5 xyz +")

    def test_traversals(self):
        t = self.build("5 3 8 * +")
        self.assertEqual([p.element() for p in t.preorder()], ["+", "5", "*", "3", "8"])
        self.assertEqual([p.element() for p in t.inorder()], ["5", "+", "3", "*", "8"])
        self.assertEqual([p.element() for p in t.postorder()], ["5", "3", "8", "*", "+"])

    def test_transfer_ownership(self):
        a, b = self.build("5"), self.build("3")
        p = a.root()
        t = BinaryExpressionTree()
        t._add_root("+")
        t.attach_subtrees(a, b)
        self.assertEqual((len(a), len(b), len(t)), (0, 0, 3))
        with self.assertRaises(ValueError):
            p.element()

    def test_navigation_and_parent_links(self):
        t = self.build("8 2 / 3 -")
        root = t.root()
        self.assertEqual(root.element(), "-")
        left, right = t.left(root), t.right(root)
        self.assertEqual(left.element(), "/")
        self.assertEqual(right.element(), "3")
        self.assertEqual(t.parent(left).element(), "-")
        self.assertEqual(t.parent(right).element(), "-")
        self.assertEqual(t.left(left).element(), "8")
        self.assertEqual(t.right(left).element(), "2")
        self.assertIsNone(t.parent(root))
        self.assertEqual(len(t), 5)

    def test_attach_rejects_aliasing(self):
        a = self.build("5")
        t = BinaryExpressionTree()
        t._add_root("+")
        with self.assertRaises(ValueError):
            t.attach_subtrees(a, a)
        self.assertEqual(len(a), 1)
        self.assertEqual(len(t), 1)

    def test_nonfinite_token_rejected(self):
        for token in ("nan", "inf", "-inf"):
            with self.subTest(token=token):
                with self.assertRaises(ValueError):
                    self.build(token)

    def test_constructor_and_float_result(self):
        t = BinaryExpressionTree("5 3 8 * +")
        self.assertEqual(t.to_postfix(), "5 3 8 * +")
        self.assertEqual(t.to_infix(), "(5 + (3 * 8))")
        self.assertEqual(t.evaluate(), 29.0)

if __name__ == "__main__":
    unittest.main()
