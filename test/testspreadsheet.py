from unittest import TestCase
from spreadsheet import SpreadSheet


class TestSpreadSheet(TestCase):

    def test_eval_int(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, 1)
        self.assertEqual(1, sheet.evaluate(cell))

    def test_eval_non_int(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, 1.5)
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_quoted_str(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "'Apple'")
        self.assertEqual("Apple", sheet.evaluate(cell))

    def test_eval_str_invalid_quote(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "'Apple")
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_str_formula(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "='Apple'")
        self.assertEqual("Apple", sheet.evaluate(cell))

    def test_eval_int_formula(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "=1")
        self.assertEqual(1, sheet.evaluate(cell))

    def test_eval_str_formula_invalid_quoting(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "='Apple")
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_formula_with_reference_to_cell(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 42
        sheet.set(cell, f"={another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual(another_cell_value, sheet.evaluate(cell))

    def test_eval_formula_with_reference_to_invalid_cell(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 42.5
        sheet.set(cell, f"={another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_formula_with_circular_reference(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = f"={cell}"
        sheet.set(cell, f"={another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Circular", sheet.evaluate(cell))

    def test_eval_formula_with_int_addition(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, f"=1+3")
        self.assertEqual(4, sheet.evaluate(cell))

    def test_eval_formula_with_invalid_types_addition(self):
        # Do not allow float addition with integers
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, f"=1+3.5")
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_formula_with_division_by_zero(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, f"=1/0")
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_formula_with_multiplication_and_addition_priority(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, f"=1+3*2")
        self.assertEqual(7, sheet.evaluate(cell))

    def test_eval_formula_with_arithmetic_and_reference(self):
        # Should get the value from B1 and perform the arithmetic operation on the two numbers
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 3
        sheet.set(cell, f"=1+{another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual(4, sheet.evaluate(cell))

    def test_eval_formula_with_arithmetic_and_invalid_reference(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 3.1
        sheet.set(cell, f"=1+{another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_formula_with_circular_arithmetic_reference(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = f"={cell}"
        sheet.set(cell, f"=1+{another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Circular", sheet.evaluate(cell))

    def test_eval_formula_with_string_concatenations(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "='Hello'&'World'")
        self.assertEqual("Hello World", sheet.evaluate(cell))

    def test_eval_formula_with_broken_string_concatenations(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "='Hello'&'World")
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_formula_with_string_concatenations_and_refs(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = "' World'"
        sheet.set(cell, f"='Hello'&{another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("Hello World", sheet.evaluate(cell))

    def test_eval_formula_with_string_concatenations_and_invalid_ref(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = " World'"
        sheet.set(cell, f"='Hello'&{another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("Hello World", sheet.evaluate(cell))

    def test_eval_formula_with_string_concatenations_and_circular_ref(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = "=A1"
        sheet.set(cell, f"='Hello'&{another_cell}")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Circular", sheet.evaluate(cell))

    def test_eval_arithmetic_formula_with_parenthesis(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "=2*(1+2)")
        self.assertEqual(6, sheet.evaluate(cell))

    def test_eval_arithmetic_formula_with_parenthesis_ws(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, "= 2 * (1 + 2)")
        self.assertEqual(6, sheet.evaluate(cell))

    def test_eval_arithmetic_formula_with_parenthesis_and_refs(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 2
        sheet.set(cell, f"=2*(1+{another_cell})")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual(6, sheet.evaluate(cell))

    def test_eval_arithmetic_formula_with_parenthesis_and_refs_ws(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 2
        sheet.set(cell, f"=2 * (1 + {another_cell})")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual(6, sheet.evaluate(cell))

    def test_eval_arithmetic_formula_with_parenthesis_and_refs_with_invalid_int(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = 2.1
        sheet.set(cell, f"=2*(1+{another_cell})")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Error", sheet.evaluate(cell))

    def test_eval_arithmetic_formula_with_parens_and_circular_ref(self):
        sheet = SpreadSheet()
        cell = "A1"
        another_cell = "B1"
        another_cell_value = f"={cell}"
        sheet.set(cell, f"=2*(1+{another_cell})")
        sheet.set(another_cell, another_cell_value)
        self.assertEqual("#Circular", sheet.evaluate(cell))
