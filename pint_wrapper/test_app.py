from unittest import TestCase
import unittest

from app import format_dimension_result, DUMMY, get_power_of_dummy_var


class TestFormat_dimension_result(TestCase):
    def test_format_dimension_result(self):
        #dummy top
        res = DUMMY + " / L"
        self.assertEqual(format_dimension_result(res).strip(), "L")
        res = "( " + DUMMY + " * T ) / L"
        self.assertEqual(format_dimension_result(res).strip(), "L / T")
        res = "( T * " + DUMMY + " ) / L"
        self.assertEqual(format_dimension_result(res).strip(), "L / T")

        #dummy bottom
        res = " T / ( V * " + DUMMY + ")"
        self.assertEqual(format_dimension_result(res).strip(), "T / V")
        res = " T / ( " + DUMMY + " * V )"
        self.assertEqual(format_dimension_result(res).strip(), "T / V")
        res = " T / " + DUMMY
        self.assertEqual(format_dimension_result(res).strip(), "T")

        #dummy power on bottom
        res = " T * V / " + DUMMY + "^5"
        self.assertEqual(format_dimension_result(res).strip(), "(T * V)^(1/5)")
        res = " T / ( V * " + DUMMY + "^5 )"
        self.assertEqual(format_dimension_result(res).strip(), "(T / V)^(1/5)")
        res = " T / " + DUMMY + "^5"
        self.assertEqual(format_dimension_result(res).strip(), "T^(1/5)")
        res = DUMMY + "^5 / T "
        self.assertEqual(format_dimension_result(res).strip(), "T^(1/5)")
        res = DUMMY + "^5 * V / T "
        self.assertEqual(format_dimension_result(res).strip(), "(T / V)^(1/5)")
        res = "V * " + DUMMY + "^5 / T "
        self.assertEqual(format_dimension_result(res).strip(), "(T / V)^(1/5)")

    def test_get_power_of_dummy_var(self):
        res = DUMMY + "^10"
        self.assertEqual(get_power_of_dummy_var(res), "10")
        res = DUMMY
        self.assertEqual(get_power_of_dummy_var(res), "")
        res = "V * " + DUMMY + "^5"
        self.assertEqual(get_power_of_dummy_var(res), "5")

if __name__ == "__main__":
    unittest.main()
