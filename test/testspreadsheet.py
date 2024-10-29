from unittest import TestCase
from spreadsheet import SpreadSheet


class TestSpreadSheet(TestCase):

    def test_eval_int(self):
        sheet = SpreadSheet()
        cell = "A1"
        sheet.set(cell, 1)
        self.assertEqual(1, sheet.evaluate(cell))
