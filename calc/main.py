# SPDX-FileCopyrightText: Calc | Copyright (c) 2026 Travis L. Seymour, PhD <nogard@ucsc.edu>
# SPDX-License-Identifier: GPL-3.0-or-later

import math
import statistics
import sys
from importlib.metadata import version
from typing import Annotated

import cyclopts
from simpleeval import simple_eval

# Build safe function dict from math and statistics modules
FUNCTIONS = {
    # Math functions
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "pow": pow,
    "sum": lambda *args: sum(args),
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    "trunc": math.trunc,
    "factorial": math.factorial,
    "gcd": math.gcd,
    "lcm": math.lcm,
    "degrees": math.degrees,
    "radians": math.radians,
    "hypot": math.hypot,
    # Statistics functions (wrapped for variadic args)
    "mean": lambda *args: statistics.mean(args),
    "median": lambda *args: statistics.median(args),
    "mode": lambda *args: statistics.mode(args),
    "stdev": lambda *args: statistics.stdev(args),
    "variance": lambda *args: statistics.variance(args),
    "pstdev": lambda *args: statistics.pstdev(args),
    "pvariance": lambda *args: statistics.pvariance(args),
    "harmonic_mean": lambda *args: statistics.harmonic_mean(args),
    "geometric_mean": lambda *args: statistics.geometric_mean(args),
}

# Constants
NAMES = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "inf": math.inf,
}

app = cyclopts.App(
    help="Commandline calculator with math and statistics functions.",
    version=f"calc {version('calc')}",
)


@app.default
def main(
    expression: Annotated[str, cyclopts.Parameter(help="Mathematical expression to evaluate")] = "",
    *,
    list_functions: Annotated[bool, cyclopts.Parameter("--list", "-l", help="List available functions")] = False,
):
    """
    Evaluate a mathematical expression.

    Examples:
        calc "3 + 4 * 2"
        calc "sqrt(2) * pi"
        calc "mean(1, 2, 3, 4, 5)"
    """
    if list_functions:
        print("Available functions:")
        print(f"  Math: {', '.join(sorted(k for k in FUNCTIONS.keys() if not k[0].islower() or k in dir(math)))}")
        print("  Stats: mean, median, mode, stdev, variance, pstdev, pvariance, harmonic_mean, geometric_mean")
        print(f"Constants: {', '.join(NAMES.keys())}")
        return

    if not expression:
        app.help_print()
        sys.exit(0)

    try:
        result = simple_eval(expression, functions=FUNCTIONS, names=NAMES)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
