import math
import statistics

import pytest
from typer.testing import CliRunner

from calc.main import FUNCTIONS, NAMES, app
from simpleeval import simple_eval

runner = CliRunner()


def evaluate(expression: str):
    """Helper to evaluate expressions using the same config as main."""
    return simple_eval(expression, functions=FUNCTIONS, names=NAMES)


class TestBasicArithmetic:
    def test_addition(self):
        assert evaluate("2 + 3") == 5

    def test_subtraction(self):
        assert evaluate("10 - 4") == 6

    def test_multiplication(self):
        assert evaluate("6 * 7") == 42

    def test_division(self):
        assert evaluate("15 / 3") == 5.0

    def test_floor_division(self):
        assert evaluate("17 // 5") == 3

    def test_modulo(self):
        assert evaluate("17 % 5") == 2

    def test_power(self):
        assert evaluate("2 ** 10") == 1024

    def test_negative_numbers(self):
        assert evaluate("-5 + 3") == -2

    def test_parentheses(self):
        assert evaluate("3 + (8 * 4.32) / 16") == pytest.approx(5.16)

    def test_complex_expression(self):
        assert evaluate("(10 + 5) * 2 - 8 / 4") == 28.0


class TestMathFunctions:
    def test_sqrt(self):
        assert evaluate("sqrt(16)") == 4.0

    def test_sin(self):
        assert evaluate("sin(0)") == 0.0

    def test_cos(self):
        assert evaluate("cos(0)") == 1.0

    def test_tan(self):
        assert evaluate("tan(0)") == 0.0

    def test_asin(self):
        assert evaluate("asin(0)") == 0.0

    def test_acos(self):
        assert evaluate("acos(1)") == 0.0

    def test_atan(self):
        assert evaluate("atan(0)") == 0.0

    def test_log(self):
        assert evaluate("log(e)") == pytest.approx(1.0)

    def test_log10(self):
        assert evaluate("log10(1000)") == 3.0

    def test_log2(self):
        assert evaluate("log2(8)") == 3.0

    def test_exp(self):
        assert evaluate("exp(0)") == 1.0

    def test_floor(self):
        assert evaluate("floor(3.7)") == 3

    def test_ceil(self):
        assert evaluate("ceil(3.2)") == 4

    def test_trunc(self):
        assert evaluate("trunc(-3.7)") == -3

    def test_factorial(self):
        assert evaluate("factorial(5)") == 120

    def test_gcd(self):
        assert evaluate("gcd(48, 18)") == 6

    def test_lcm(self):
        assert evaluate("lcm(4, 6)") == 12

    def test_degrees(self):
        assert evaluate("degrees(pi)") == pytest.approx(180.0)

    def test_radians(self):
        assert evaluate("radians(180)") == pytest.approx(math.pi)

    def test_hypot(self):
        assert evaluate("hypot(3, 4)") == 5.0

    def test_abs(self):
        assert evaluate("abs(-42)") == 42

    def test_round(self):
        assert evaluate("round(3.14159, 2)") == 3.14

    def test_min(self):
        assert evaluate("min(5, 3, 8, 1)") == 1

    def test_max(self):
        assert evaluate("max(5, 3, 8, 1)") == 8

    def test_pow(self):
        assert evaluate("pow(2, 3)") == 8

    def test_sum(self):
        assert evaluate("sum(1, 2, 3, 4)") == 10


class TestStatisticsFunctions:
    def test_mean(self):
        assert evaluate("mean(2, 4, 6)") == 4.0

    def test_median_odd(self):
        assert evaluate("median(1, 3, 5)") == 3

    def test_median_even(self):
        assert evaluate("median(1, 2, 3, 4)") == 2.5

    def test_mode(self):
        assert evaluate("mode(1, 2, 2, 3)") == 2

    def test_stdev(self):
        result = evaluate("stdev(2, 4, 6, 8)")
        expected = statistics.stdev([2, 4, 6, 8])
        assert result == pytest.approx(expected)

    def test_variance(self):
        result = evaluate("variance(2, 4, 6, 8)")
        expected = statistics.variance([2, 4, 6, 8])
        assert result == pytest.approx(expected)

    def test_pstdev(self):
        result = evaluate("pstdev(2, 4, 6, 8)")
        expected = statistics.pstdev([2, 4, 6, 8])
        assert result == pytest.approx(expected)

    def test_pvariance(self):
        result = evaluate("pvariance(2, 4, 6, 8)")
        expected = statistics.pvariance([2, 4, 6, 8])
        assert result == pytest.approx(expected)

    def test_harmonic_mean(self):
        result = evaluate("harmonic_mean(2, 4, 8)")
        expected = statistics.harmonic_mean([2, 4, 8])
        assert result == pytest.approx(expected)

    def test_geometric_mean(self):
        result = evaluate("geometric_mean(2, 4, 8)")
        expected = statistics.geometric_mean([2, 4, 8])
        assert result == pytest.approx(expected)


class TestConstants:
    def test_pi(self):
        assert evaluate("pi") == pytest.approx(math.pi)

    def test_e(self):
        assert evaluate("e") == pytest.approx(math.e)

    def test_tau(self):
        assert evaluate("tau") == pytest.approx(math.tau)

    def test_inf(self):
        assert evaluate("inf") == math.inf

    def test_constants_in_expressions(self):
        assert evaluate("sqrt(2) * pi") == pytest.approx(math.sqrt(2) * math.pi)


class TestCombinedExpressions:
    def test_math_with_statistics(self):
        assert evaluate("3 + mean(3, 4, 2) * 2") == 9.0

    def test_nested_functions(self):
        assert evaluate("sqrt(abs(-16))") == 4.0

    def test_trig_with_constants(self):
        assert evaluate("sin(pi / 2)") == pytest.approx(1.0)

    def test_complex_stats_expression(self):
        result = evaluate("mean(1, 2, 3) + median(4, 5, 6)")
        assert result == pytest.approx(2.0 + 5.0)


class TestErrorHandling:
    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            evaluate("1 / 0")

    def test_undefined_name(self):
        with pytest.raises(Exception):
            evaluate("undefined_var")

    def test_undefined_function(self):
        with pytest.raises(Exception):
            evaluate("unknown_func(5)")

    def test_sqrt_negative(self):
        with pytest.raises(ValueError):
            evaluate("sqrt(-1)")

    def test_factorial_negative(self):
        with pytest.raises(ValueError):
            evaluate("factorial(-5)")

    def test_stdev_single_value(self):
        with pytest.raises(statistics.StatisticsError):
            evaluate("stdev(5)")


class TestMainFunction:
    def test_main_no_args(self):
        result = runner.invoke(app, [])
        # Exit code 2 = missing required argument, but help is shown
        assert result.exit_code == 2
        assert "Usage:" in result.output

    def test_main_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Mathematical expression" in result.output

    def test_main_valid_expression(self):
        result = runner.invoke(app, ["2 + 2"])
        assert result.exit_code == 0
        assert result.output.strip() == "4"

    def test_main_invalid_expression(self):
        result = runner.invoke(app, ["invalid_expr"])
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_main_list_functions(self):
        result = runner.invoke(app, ["--list"])
        assert result.exit_code == 0
        assert "Available functions:" in result.output


class TestSecurity:
    """Verify that dangerous operations are blocked."""

    def test_import_blocked(self):
        with pytest.raises(Exception):
            evaluate("__import__('os')")

    def test_eval_blocked(self):
        with pytest.raises(Exception):
            evaluate("eval('2+2')")

    def test_exec_blocked(self):
        with pytest.raises(Exception):
            evaluate("exec('x=1')")

    def test_attribute_access_blocked(self):
        with pytest.raises(Exception):
            evaluate("''.join(['a'])")

    def test_dunder_blocked(self):
        with pytest.raises(Exception):
            evaluate("().__class__")
