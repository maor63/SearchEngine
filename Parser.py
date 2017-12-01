import re
from datetime import datetime
from itertools import groupby


class Parser:
    def __init__(self):
        self.contain_number = re.compile(".*\d.*")
        self.delimiter = re.compile("[ \t\n]")
        self.redundant_signs = re.compile("[|@^!?,*;'\"]")
        self.spacial_signs = re.compile("[&:()+=\]\[]|\.\.+")
        self.normal_date = re.compile("\d+/\d+|\d+/\d+/\d+")
        self.number_next_to_letter = re.compile(".*\d[a-zA-Z]+")

    def parse(self, text):
        text = self.redundant_signs.sub('', text)
        text = self.spacial_signs.sub(' ', text)
        text = text.replace(' .', ' ').replace('. ', ' ')
        raw_terms = self.delimiter.split(text)
        terms = set()
        number_buffer = ""
        date_buffer = ""
        upper_case_buffer = ""
        for raw_term in raw_terms:
            if raw_term == '':
                continue
            try:
                if '-' in raw_term:
                    terms.add(raw_term.lower().replace('-', ' '))
                    [terms.add(term) for term in raw_term.lower().split('-')]
                elif self.contain_number.match(raw_term):
                    date_buffer, number_buffer = self._parse_token_with_number(raw_term, date_buffer, number_buffer,
                                                                               terms)
                else:
                    date_buffer = self._flush_date_buffer(date_buffer, terms)
                    if raw_term == 'percent' or raw_term == 'percentage':
                        terms.add(number_buffer + " percent")
                        number_buffer = ""
                    elif self._is_month(raw_term):
                        date_buffer = (number_buffer + " " + raw_term).strip()
                        number_buffer = ""
                    else:
                        number_buffer = self._flush_buffer(number_buffer, terms)
                        if not raw_term[0].islower():
                            raw_term = raw_term.lower()
                            if upper_case_buffer != "":
                                terms.add(upper_case_buffer + " " + raw_term)
                                upper_case_buffer = ""
                            else:
                                upper_case_buffer = raw_term
                        else:
                            upper_case_buffer = self._flush_buffer(upper_case_buffer, terms)
                        terms.add(raw_term)
            except ValueError as e:
                print(e)
        self._flush_date_buffer(date_buffer, terms)
        self._flush_buffer(number_buffer, terms)
        self._flush_buffer(upper_case_buffer, terms)
        return terms

    def _flush_buffer(self, number, terms):
        if number != "":
            terms.add(number)
            number = ""
        return number

    def _flush_date_buffer(self, date_buffer, terms):
        if date_buffer != "":
            terms.add(self._parse_date(date_buffer))
            date_buffer = ""
        return date_buffer

    def _parse_token_with_number(self, raw_term, date_buffer, number, terms):
        raw_term = raw_term.replace('th', '')
        raw_term = raw_term.replace('O', '0')
        if self._is_number(raw_term):
            if date_buffer != "" and len(date_buffer.split(' ')) < 3:
                date_buffer += " " + raw_term
            else:
                if number != "":
                    terms.add(number)
                number = self._parse_number(raw_term)

        elif '/' in raw_term:
            if self.normal_date.match(raw_term):
                terms.add(raw_term)
            else:
                [self._parse_token_with_number(term, date_buffer, number, terms) for term in raw_term.split('/')]
        elif '$' in raw_term:
            if re.match("\$\d+b.*|\$\d+\.\d+b.*", raw_term):
                terms.add(raw_term[raw_term.find("$") + 1:raw_term.find("b")] + " dollar")
                terms.add("billion")
            elif re.match("\$\d+m.*|\$\d+\.\d+m.*", raw_term):
                terms.add(raw_term[raw_term.find("$") + 1:raw_term.find("m")] + " dollar")
                terms.add("million")
            else:
                raw_term = raw_term[raw_term.find("$"):]
                terms.add(self._parse_number(raw_term.replace('$', '')) + " dollar")
        elif '%' in raw_term:
            terms.add(self._parse_precentage(raw_term, '%'))
        else:
            terms.add(raw_term)
        return date_buffer, number

    def _parse_precentage(self, token, type):
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
        if self._is_number(date[0]):
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

    def _is_month(self, raw_term):
        try:
            if len(raw_term) > 3:
                datetime.strptime(raw_term, "%B")
            else:
                datetime.strptime(raw_term, "%b")
            return True
        except ValueError:
            return False

    def _is_number(self, raw_term):
        try:
            float(raw_term)
            return True
        except ValueError:
            return False
