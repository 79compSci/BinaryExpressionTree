"""Run a set of postfix expressions and continue after errors."""
from binary_expression_tree import BinaryExpressionTree

def main():
    for expression in ("5 3 8 * +", "8 2 / 3 -", "-2.5 4 *", "5 +", "5 3 2 +", "8 0 /", "5 abc +", ""):
        print("Input:", repr(expression))
        try:
            tree = BinaryExpressionTree.from_postfix(expression)
            print("Infix:", tree.to_infix())
            print("Postfix:", tree.to_postfix())
            print("Result:", tree.evaluate())
        except (ValueError, ZeroDivisionError) as exc:
            print(type(exc).__name__ + ":", exc)
        print()

if __name__ == "__main__":
    main()
