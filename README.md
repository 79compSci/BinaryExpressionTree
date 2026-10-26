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
