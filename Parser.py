import re
from datetime import datetime


class Parser:
    def __init__(self):
        self.contain_number = re.compile(".*\d.*")
        self.delimiter = re.compile("\s*")
        self.redundant_signs = re.compile("[():|@^!?&]")

    def parse_text(self, text):
        text = self.redundant_signs.sub('', text)
        raw_terms = self.delimiter.split(text)
        terms = []
        upper_case_buffer = []
        date_buffer = []
        for raw_term in raw_terms:
            try:
                if '-' in raw_term:
                    self.parse_connected(terms, raw_term)
                elif self.is_part_of_date(raw_term):
                    date_buffer.append(raw_term)
                elif '$' in raw_term:
                    terms.append(self.parse_token(raw_term))
                elif self.is_upper_case(raw_term):
                    upper_case_buffer.append(raw_term)
                else:
                    self.parse_buffers(date_buffer, upper_case_buffer, terms)
                    date_buffer = []
                    upper_case_buffer = []
                    terms.append(raw_term)
            except:
                terms.append(raw_term)
        self.parse_buffers(date_buffer, upper_case_buffer, terms)
        return terms

    def is_upper_case(self, raw_term):
        return not raw_term.islower() and '.' not in raw_term

    def parse_buffers(self, date_buffer, upper_case_buffer, terms):
        if len(upper_case_buffer) > 3:
            [terms.append(self.parse_token(term)) for term in upper_case_buffer]
        elif len(upper_case_buffer) != 0:
            self.parse_upper_case_buffer(upper_case_buffer, terms)
        if len(date_buffer) != 0:
            self.parse_date_buffer(date_buffer, terms)

    def parse_date_buffer(self, date_buffer, terms):
        token = " ".join(date_buffer)
        terms.append(self.parse_token(token))

    def parse_upper_case_buffer(self, buffer, terms):
        token = " ".join(buffer)
        self.parse_upper_case(terms, token)

    def parse_upper_case(self, terms, token):
        term = self.parse_token(token)
        terms.append(term)
        if ' ' in token:
            [terms.append(self.parse_token(term)) for term in token.split(' ')]

    def parse_token(self, token):
        if self.contain_number.match(token):
            token = token.replace(',', '')
            if '%' in token:
                return self.parse_precentage(token, '%')
            elif 'percentage' in token:
                return self.parse_precentage(token, 'percentage')
            elif 'percent' in token:
                return self.parse_precentage(token, 'percent')
            elif '-' in token:
                return token
            elif '$' in token:
                return self._parse_number(token.replace('$', '')) + " dollar"
            elif self.is_number(token):
                return self._parse_number(token)
            return self._parse_date(token)
        else:
            return token.lower()

    def parse_precentage(self, token, type):
        return self._parse_number(token.replace(type, '')) + ' percent'

    def _parse_number(self, token):
        return self._parse_float(float(token))

    def _parse_date(self, token):
        try:
            if '/' in token:
                return token
            token = token.replace('th', '')
            return self._parse_day_month_year_date(token)
        except Exception:
            return token

    def _parse_day_month_year_date(self, token):
        input_format = ''
        output_format = ''
        date = token.split(' ')
        if self.is_number(date[0]):
            input_format, output_format = self._day_first(date, input_format, output_format)
        else:
            input_format, output_format = self._month_first(date, input_format, output_format)
        if len(date) > 2:
            year = date[2]
            input_format, output_format = self._year_last(year, input_format, output_format)

        return self._parse_date_by_format(token, input_format, output_format)

    def _month_first(self, date, input_format, output_format):
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
            input_format, output_format = self._year_last(year, input_format, output_format)
        return input_format, output_format

    def _year_last(self, year, input_format, output_format):
        output_format += "/%Y"
        if len(year) <= 2:
            input_format += ' %y'
        else:
            input_format += ' %Y'
        return input_format, output_format

    def _day_first(self, date, input_format, output_format):
        input_format += '%d'
        output_format += '%d/%m'
        month = date[1]
        if len(month) > 3:
            input_format += ' %B'
        else:
            input_format += ' %b'
        return input_format, output_format

    def _parse_date_by_format(self, token, input_format, output_format):
        return datetime.strptime(token, input_format).strftime(output_format)

    def _parse_float(self, f):
        frac_result = str(format(f, ".2f"))
        return frac_result.replace('.00', '')

    def is_month(self, raw_term):
        try:
            if len(raw_term) > 3:
                datetime.strptime(raw_term, "%B")
            else:
                datetime.strptime(raw_term, "%b")
            return True
        except ValueError:
            return False

    def is_part_of_date(self, raw_term):
        return self.is_number(raw_term) or self.is_month(raw_term)

    def is_number(self, raw_term):
        try:
            float(raw_term)
            return True
        except ValueError:
            return False

    def parse_connected(self, terms, token):
        term = self.parse_token(token)
        terms.append(term)
        if '-' in token:
            [terms.append(self.parse_token(term)) for term in token.split('-')]
