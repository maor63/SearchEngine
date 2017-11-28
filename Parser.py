import re
from datetime import datetime


class Parser:
    def __init__(self):
        self.pattern = re.compile(".*\d.*")

    def parse_token(self, token):
        if self.pattern.match(token):
            token = token.replace(',', '')
            if '%' in token:
                return self.parse_precentage(token, '%')
            elif 'percentage' in token:
                return self.parse_precentage(token, 'percentage')
            elif 'percent' in token:
                return self.parse_precentage(token, 'percent')
            return self._parse_number(token)
        else:
            return token

    def parse_precentage(self, token, type):
        return self._parse_number(token.replace(type, '')) + ' percent'

    def _parse_number(self, token):
        try:
            return self._parse_float(float(token))
        except ValueError:
            return self._parse_date(token)

    def _parse_date(self, token):
        if '/' in token:
            return token
        token = token.replace('th', '')
        return self._parse_day_month_year_date(token)

    def _parse_day_month_year_date(self, token):
        input_format = ''
        output_format = ''
        date = token.split(' ')
        if date[0].isdigit():
            input_format, output_format = self.day_first(date, input_format, output_format)
        else:
            input_format, output_format = self.month_first(date, input_format, output_format)
        if len(date) > 2:
            year = date[2]
            input_format, output_format = self.year_last(year, input_format, output_format)

        return self._parse_date_by_format(input_format, token, output_format)

    def month_first(self, date, input_format, output_format):
        month = date[0]
        output_format += '%m'
        if len(month) > 3:
            input_format += '%B'
        else:
            input_format += '%b'
        if len(date[1]) <= 2 and int(date[1]) <= 31:
            input_format += ' %d'
            output_format = "%d/" + output_format
        else:
            year = date[1]
            input_format, output_format = self.year_last(year, input_format, output_format)
        return input_format, output_format

    def year_last(self, year, input_format, output_format):
        output_format += "/%Y"
        if len(year) <= 2:
            input_format += ' %y'
        else:
            input_format += ' %Y'
        return input_format, output_format

    def day_first(self, date, input_format, output_format):
        input_format += '%d'
        output_format += '%d/%m'
        month = date[1]
        if len(month) > 3:
            input_format += ' %B'
        else:
            input_format += ' %b'
        return input_format, output_format

    def _parse_date_by_format(self, format, token, output_format="%d/%m/%Y"):
        return datetime.strptime(token, format).strftime(output_format)

    def _parse_float(self, f):
        frac_result = str(format(f, ".2f"))
        return frac_result.replace('.00', '')
