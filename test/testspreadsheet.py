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
