import unittest

from Parser import Parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_rational_number(self):
        parser = Parser()
        result = parser.parse_token("3.55555")
        self.assertEqual("3.56", result)

    def test_parse_fraction(self):
        result = self.parser.parse_token("2/3")
        self.assertEqual("0.67", result)

    def test_parse_big_numbers(self):
        result = self.parser.parse_token("1,345")
        self.assertEqual("1345", result)

    def test_parse_number(self):
        result = self.parser.parse_token("14")
        self.assertEqual("14", result)

    def test_parse_present_type_1(self):
        result = self.parser.parse_token("6%")
        self.assertEqual("6 percent", result)

    def test_parse_present_type_2(self):
        result = self.parser.parse_token("12,550.666 percent")
        self.assertEqual("12550.67 percent", result)

    def test_parse_present_type_3(self):
        result = self.parser.parse_token("12,550.666 percentage")
        self.assertEqual("12550.67 percent", result)

    def test_parse_date_type_1(self):
        result = self.parser.parse_token("12th MAY 1991")
        self.assertEqual("12/05/1991", result)

    def test_parse_date_type_2(self):
        result = self.parser.parse_token("16 FEB 1991")
        self.assertEqual("16/02/1991", result)

    def test_parse_date_type_3(self):
        result = self.parser.parse_token("13 May 91")
        self.assertEqual("13/05/1991", result)

    def test_parse_date_type_4(self):
        result = self.parser.parse_token("Feb 12, 1990")
        self.assertEqual("12/02/1990", result)

    def test_parse_date_type_5(self):
        result = self.parser.parse_token("12th Jan 1991")
        self.assertEqual("12/01/1991", result)

    def test_parse_date_type_6(self):
        result = self.parser.parse_token("30 September 2006")
        self.assertEqual("30/09/2006", result)

    def test_parse_date_type_7(self):
        result = self.parser.parse_token("21 DEC 09")
        self.assertEqual("21/12/2009", result)

    def test_parse_date_type_8(self):
        result = self.parser.parse_token("JUNE 15, 2000")
        self.assertEqual("15/06/2000", result)

    def test_parse_date_type_9(self):
        result = self.parser.parse_token("01 Aug 1880")
        self.assertEqual("01/08/1880", result)

    def test_parse_date_type_10(self):
        result = self.parser.parse_token("08th July 2017")
        self.assertEqual("08/07/2017", result)




if __name__ == '__main__':
    unittest.main()
