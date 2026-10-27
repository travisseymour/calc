# SPDX-FileCopyrightText: Calc | Copyright (c) 2026 Travis L. Seymour, PhD <nogard@ucsc.edu>
# SPDX-License-Identifier: GPL-3.0-or-later

import ast
import re


def decompose_expression(expression: str, functions: dict, names: dict) -> list[str]:
    """
    Decompose an expression into evaluation steps.

    Returns a list of strings showing the progression from original
    expression to final result, with function calls replaced by their values.
    """
    from simpleeval import simple_eval

    steps = [expression]
    current = expression

    # Keep replacing function calls until none remain
    while True:
        # Find innermost function calls (functions with no nested function calls in args)
        pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\(([^()]*)\)"
        matches = list(re.finditer(pattern, current))

        if not matches:
            break

        # Process all innermost function calls in this pass
        new_expr = current
        offset = 0

        for match in matches:
            func_name = match.group(1)
            if func_name not in functions:
                continue

            # Evaluate just this function call
            full_match = match.group(0)
            try:
                value = simple_eval(full_match, functions=functions, names=names)
                value_str = repr(value) if isinstance(value, str) else str(value)

                # Replace in the expression, adjusting for previous replacements
                start = match.start() + offset
                end = match.end() + offset
                new_expr = new_expr[:start] + value_str + new_expr[end:]
                offset += len(value_str) - len(full_match)
            except Exception:
                continue

        if new_expr != current:
            current = new_expr
            steps.append(current)
        else:
            break

    # Final evaluation
    try:
        result = simple_eval(current, functions=functions, names=names)
        result_str = repr(result) if isinstance(result, str) else str(result)
        if steps[-1] != result_str:
            steps.append(result_str)
    except Exception:
        pass

    return steps


def print_decomposition(expression: str, functions: dict, names: dict) -> None:
    """Print the step-by-step decomposition of an expression."""
    steps = decompose_expression(expression, functions, names)
    for step in steps:
        print(step)
