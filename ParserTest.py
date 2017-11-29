import unittest

from Parser import Parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_rational_number(self):
        parser = Parser()
        result = parser.parse_token("3.55555")
        self.assertEqual("3.56", result)

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

    def test_parse_date_type_11(self):
        result = self.parser.parse_token("04 MAY")
        self.assertEqual("04/05", result)

    def test_parse_date_type_12(self):
        result = self.parser.parse_token("June 4")
        self.assertEqual("04/06", result)

    def test_parse_date_type_13(self):
        result = self.parser.parse_token("May 1994")
        self.assertEqual("05/1994", result)

    def test_parse_date_normal_month_year(self):
        result = self.parser.parse_token("05/1994")
        self.assertEqual("05/1994", result)

    def test_parse_date_normal_day_month(self):
        result = self.parser.parse_token("14/05")
        self.assertEqual("14/05", result)

    def test_parse_date_normal_day_month_year(self):
        result = self.parser.parse_token("12/05/1991")
        self.assertEqual("12/05/1991", result)

    def test_parse_date_month_day(self):
        result = self.parser.parse_token("sep 07")
        self.assertEqual("07/09", result)

    def test_parse_text_with_upper_case_words(self):
        text = "Jiang Zemin today the Chinese Army to strengthen"
        result = self.parser.parse_text(text)
        expected = ["jiang zemin", "jiang", "zemin", "today", "the", "chinese army", "chinese", "army", "to",
                    "strengthen"]
        self.assertListEqual(result, expected)

    def test_parse_text_with_dates(self):
        text = "3 mission 5 NBA of 12 September 2006 and JULY 22 win 33-44 test-case"
        result = self.parser.parse_text(text)
        expected = ["3", "mission", "nba", "5", "of", "12/09/2006", "and", "22/07", "win", "33-44", "33", "44",
                    "test-case", "test", "case"]
        self.assertListEqual(result, expected)

    def test_parse_text(self):
        text = '''Jiang Zemin 5.79 today the Chinese Army 4 to strengthen its
    own building mission of 12 September 2006 and JULY 22
    after May 11 1999 at the 4 SEP and JUNE 2005'''
        result = self.parser.parse_text(text)
        expected = ["jiang zemin", "jiang", "zemin", "5.79", "today", "the", "chinese army", "chinese", "army", "4",
                    "to", "strengthen", "its", "own", "building", "mission", "of", "12/09/2006", "and", "22/07",
                    "after", "11/05/1999", "at", "the", "04/09", "and", "06/2005"]
        self.assertListEqual(result, expected)

    def test_parse_text_with_dollar(self):
        text = "hello to all of you i am $20 min away"
        result = self.parser.parse_text(text)
        expected = ["hello", "to", "all", "of", "you", "i", "am", "20 dollar", "min", "away"]
        self.assertListEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
