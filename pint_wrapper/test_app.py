from unittest import TestCase
import unittest

from app import format_dimension_result, DUMMY


class TestFormat_dimension_result(TestCase):
    def test_format_dimension_result(self):
        res = DUMMY + " / L"
        self.assertEqual(format_dimension_result(res).strip(), "L")
        res = DUMMY + " * T / L"
        self.assertEqual(format_dimension_result(res).strip(), "L/T")
        res = "T * " + DUMMY + " / L"
        self.assertEqual(format_dimension_result(res).strip(), "L/T")
        res = " T / V * " + DUMMY
        self.assertEqual(format_dimension_result(res).strip(), "T / V")
        res = " T / " + DUMMY
        self.assertEqual(format_dimension_result(res).strip(), "T")

if __name__ == "__main__":
    unittest.main()
