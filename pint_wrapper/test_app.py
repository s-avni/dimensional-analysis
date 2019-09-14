from unittest import TestCase
import unittest

from app import format_dimension_result, DUMMY, get_power_of_dummy_var, \
    get_complete_dim_word, SHORTCUT_DICT, get_word_partition, replace_acronyms_and_return_word
from pint import UnitRegistry, formatter, pi_theorem


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

    def test_get_complete_dim_word(self):
        for key in SHORTCUT_DICT:
            self.assertEqual(get_complete_dim_word(key), SHORTCUT_DICT[key])
            key_with_spaces = " ".join(key)
            self.assertEqual(get_complete_dim_word(key_with_spaces), SHORTCUT_DICT[key])

    def test_get_word_partition(self):
        self.assertEqual(get_word_partition("[T] / [V]"), ["[T]", " / " , "[V]"])
        self.assertEqual(get_word_partition("[T] * [M] / [V]"), ["[T]", " * ", "[M]"," / ", "[V]"])

    def test_replace_acronyms_and_return_word(self):
        self.assertEqual(replace_acronyms_and_return_word(["[t]"]),"[time]")
        self.assertEqual(replace_acronyms_and_return_word(["[t]", " * ", "[M]"]), "[time] * [mass]")

    def test_pi_theorem(self):
        ureg = UnitRegistry()
        quantities = {"Va": "[time]", "Vb": "[length]", "Vc": "[length] / [time]"}
        pi = pi_theorem(quantities, ureg)
        pretty_result = formatter(pi[0].items(), single_denominator=True, power_fmt='{}^{}')
        self.assertEqual(pretty_result, "Va * Vc / Vb")

        quantities = {"Va" : "[time]", "Vb" : "[length]", "Vc" : "[acceleration]"}
        pi = pi_theorem(quantities, ureg)
        pretty_result = formatter(pi[0].items(), single_denominator=True, power_fmt='{}^{}')
        self.assertEqual(pretty_result, "Va^2 * Vc / Vb")

    def test_get_power_of_dummy_var(self):
        res = DUMMY + "^10"
        self.assertEqual(get_power_of_dummy_var(res), "10")
        res = DUMMY
        self.assertEqual(get_power_of_dummy_var(res), "")
        res = "V * " + DUMMY + "^5"
        self.assertEqual(get_power_of_dummy_var(res), "5")

if __name__ == "__main__":
    unittest.main()
