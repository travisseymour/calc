"""
Calc: Commandline calculator utility with basic python math and statistics functions.
Copyright (C) 2026  Travis L. Seymour, PhD

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math
import statistics
from typing import Annotated, Optional

import typer
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


app = typer.Typer(
    help="Commandline calculator with math and statistics functions.",
    add_completion=False,
    no_args_is_help=True,
)


def version_callback(value: bool):
    if value:
        from importlib.metadata import version

        print(f"calc {version('calc')}")
        raise typer.Exit()


def list_functions_callback(value: bool):
    if value:
        print("Available functions:")
        print(f"  Math: {', '.join(sorted(k for k in FUNCTIONS.keys() if not k[0].islower() or k in dir(math)))}")
        print("  Stats: mean, median, mode, stdev, variance, pstdev, pvariance, harmonic_mean, geometric_mean")
        print(f"Constants: {', '.join(NAMES.keys())}")
        raise typer.Exit()


@app.command()
def main(
    expression: Annotated[str, typer.Argument(help="Mathematical expression to evaluate")],
    version: Annotated[
        Optional[bool], typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show version")
    ] = None,
    list_functions: Annotated[
        Optional[bool],
        typer.Option("--list", "-l", callback=list_functions_callback, is_eager=True, help="List available functions"),
    ] = None,
):
    """
    Evaluate a mathematical expression.

    Examples:
        calc "3 + 4 * 2"
        calc "sqrt(2) * pi"
        calc "mean(1, 2, 3, 4, 5)"
    """
    try:
        result = simple_eval(expression, functions=FUNCTIONS, names=NAMES)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
