# Binary Expression Tree — CSC 223

Construct a linked positional binary expression tree from whitespace-separated postfix notation.

## Run

```bash
python main.py
python -m unittest discover -v
```

## Features

- Numeric operands, including negative numbers and decimals
- Binary operators `+ - * /`
- Postfix-to-tree construction using the reused `Stack` class
- Fully parenthesized infix and regenerated postfix
- Recursive evaluation, preorder, inorder, postorder position traversals

## Error handling

`ValueError` for empty expressions, unsupported tokens, too few operands, or extra operands.
`ZeroDivisionError` for division by zero during evaluation.

## Design

When an operator is read, the first popped subtree is its RIGHT child and the second is its LEFT child.
Subtree attachment transfers nodes without copying, empties both source trees, and invalidates positions in those source trees. Raw inorder traversal does not insert parentheses.

The stack implementation is reused from [79compSci/Stack](https://github.com/79compSci/Stack).

## Academic integrity

Review and understand the implementation and run tests yourself. Document your actual test results and disclose substantive AI assistance in the submitted report as required by the course policy.

## Test coverage

The unit test suite includes addition, nested operators, subtraction/division operand order, decimals and negatives, invalid postfix expressions, division by zero, postfix round-tripping, traversals, positional parent/child navigation, subtree ownership, constructor behavior, and rejection of non-finite numeric tokens.

GitHub Actions runs `python -m unittest discover -v` after pushes and pull requests. Open the **Actions** tab to see the actual pass/fail result.

## Complexity

For `n` postfix tokens, building the tree and evaluating or traversing it each take `O(n)` time. Storage takes `O(n)` space for the tree. Recursive traversal uses `O(h)` additional call-stack space, where `h` is the tree height. Fully parenthesized infix creation may incur additional copying cost from repeated string concatenation.

## Representative expected results

| Postfix | Fully parenthesized infix | Expected evaluation |
| --- | --- | --- |
| `5 3 8 * +` | `(5 + (3 * 8))` | `29.0` |
| `8 2 / 3 -` | `((8 / 2) - 3)` | `1.0` |

These are expected values, not a substitute for recorded test-run evidence. Copy the actual unittest output into your report after running it.

## AI assistance disclosure

AI assistance was used to review and extend test coverage and documentation. Check the implementation, understand its behavior, and accurately describe your own contributions and test evidence according to the course policy.
