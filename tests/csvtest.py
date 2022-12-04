import unittest
from speciallectureis.csvsample import CSVPrinter


class TestCSVPrinter(unittest.TestCase):
    def test_method1(self):
        printer = CSVPrinter("sample.csv")
        lines = printer.read()
        self.assertEqual(3, len(lines))

    def test_method2(self):
        printer = CSVPrinter("sample.csv")
        lines = printer.read()
        self.assertEqual("value2B", lines[1][1])

    def test_method3(self):
        printer = CSVPrinter("sample.tsv")
        lines = printer.read(tsv=True)
        self.assertEqual("value2B", lines[1][1])

    def test_method4(self):
        with self.assertRaises(FileNotFoundError):
            printer = CSVPrinter("not_exist.csv")
            printer.read()
