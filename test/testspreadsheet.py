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

