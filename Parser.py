import os
import re
from datetime import datetime


class Parser:
    def __init__(self, stop_word_path):
        self.contain_number = re.compile(".*\d.*")
        self.delimiter = re.compile("[ \t\n]")
        self.redundant_signs = re.compile("[|@^!?,*;'\"]")
        self.spacial_signs = re.compile("[&:()+=\]\[]|\.\.+")
        self.normal_date = re.compile("\d+/\d+|\d+/\d+/\d+")
        self.number_next_to_letter = re.compile(".*\d[a-zA-Z]+")
        self.empty_term = re.compile("\s*")

        self.init_data_structures()
        self.stop_words = self._set_of_stopwords(stop_word_path)

    def _set_of_stopwords(self, path):
        if not os.path.exists(path):
            return set()
        with open(path) as f:
            return set((line.strip() for line in f.readlines()))

    def parse(self, text):
        text = self.redundant_signs.sub('', text)
        text = self.spacial_signs.sub(' ', text)
        text = text.replace(' .', ' ').replace('. ', ' ')
        raw_terms = self.delimiter.split(text)

        self.init_data_structures()
        return self._parse_raw_terms(raw_terms)

    def _parse_raw_terms(self, raw_terms):
        for raw_term in raw_terms:
            try:
                self._parse_token(raw_term)
            except ValueError as e:
                print(e)
        self._flush_date_buffer(self._date_buffer, self.terms)
        self._flush_buffer(self._number_buffer, self.terms)
        self._flush_buffer(self._upper_case_buffer, self.terms)
        self._delete_empty_terms()
        return self.terms

    def _delete_empty_terms(self):
        copy = self.terms.copy()
        for term in copy:
            if term == '' or term == ' ' or term == '  ':
                del self.terms[term]

    def init_data_structures(self):
        self.terms = {}
        self._date_buffer = ""
        self._number_buffer = ""
        self._upper_case_buffer = ""

    def _parse_token(self, raw_term):
        if raw_term == '' or raw_term == ' ' or raw_term == '  ':
            return
        elif '-' in raw_term:
            term = raw_term.lower().replace('-', ' ').strip()
            if not self.contain_number.match(term):
                self.add_to_dict(term, self.terms)
            [self._parse_token(term) for term in raw_term.lower().split('-')]
        elif self.contain_number.match(raw_term):
            self._token_with_number(raw_term)
        else:
            self._token_without_number(raw_term)

    def _token_without_number(self, raw_term):
        self._date_buffer = self._flush_date_buffer(self._date_buffer, self.terms)
        if raw_term == 'percent' or raw_term == 'percentage':
            self.add_to_dict((self._number_buffer + " percent"), self.terms)
            self._number_buffer = ""
        elif self._is_month(raw_term):
            self._date_buffer = (self._number_buffer + " " + raw_term).strip()
            self._number_buffer = ""
        else:
            self._number_buffer = self._flush_buffer(self._number_buffer, self.terms)
            if not raw_term[0].islower():
                raw_term = raw_term.lower()
                if self._upper_case_buffer != "":
                    self.add_to_dict((self._upper_case_buffer + " " + raw_term), self.terms)
                    self._upper_case_buffer = ""
                else:
                    self._upper_case_buffer = raw_term
            else:
                self._upper_case_buffer = self._flush_buffer(self._upper_case_buffer, self.terms)
            self.add_to_dict(raw_term, self.terms)

    def _token_with_number(self, raw_term):
        raw_term = raw_term.replace('th', '')
        raw_term = raw_term.replace('O', '0')
        if self._is_number(raw_term):
            if self._date_buffer != "" and len(self._date_buffer.split(' ')) < 3:
                self._date_buffer += " " + raw_term
            else:
                if self._number_buffer != "":
                    self.add_to_dict(self._number_buffer, self.terms)
                self._number_buffer = self._parse_number(raw_term)

        elif '/' in raw_term:
            if self.normal_date.match(raw_term):
                self.add_to_dict(raw_term, self.terms)
            else:
                [self._parse_token_with_number(term, self._date_buffer, self._number_buffer, self.terms) for term in
                 raw_term.split('/')]
        elif '$' in raw_term:
            if re.match("\$\d+b.*|\$\d+\.\d+b.*", raw_term):
                self.add_to_dict((raw_term[raw_term.find("$") + 1:raw_term.find("b")] + " dollar"), self.terms)
                self.add_to_dict("billion", self.terms)
            elif re.match("\$\d+m.*|\$\d+\.\d+m.*", raw_term):
                self.add_to_dict((raw_term[raw_term.find("$") + 1:raw_term.find("m")] + " dollar"), self.terms)
                self.add_to_dict("million", self.terms)
            else:
                raw_term = raw_term[raw_term.find("$") + 1:]
                self.add_to_dict((self._parse_number(raw_term.replace('$', '')) + " dollar"), self.terms)
        elif '%' in raw_term:
            self.add_to_dict((self._parse_precentage(raw_term, '%')), self.terms)
        else:
            self.add_to_dict(raw_term, self.terms)

    def _flush_buffer(self, number, terms):
        if number != "":
            self.add_to_dict(number, terms)
            number = ""
        return number

    def _flush_date_buffer(self, date_buffer, terms):
        if date_buffer != "":
            self.add_to_dict((self._parse_date(date_buffer)), terms)
            date_buffer = ""
        return date_buffer

    def _parse_token_with_number(self, raw_term, date_buffer, number_buffer, terms):
        raw_term = raw_term.replace('th', '')
        raw_term = raw_term.replace('O', '0')
        if self._is_number(raw_term):
            if date_buffer != "" and len(date_buffer.split(' ')) < 3:
                date_buffer += " " + raw_term
            else:
                if number_buffer != "":
                    self.add_to_dict(number_buffer, terms)
                number_buffer = self._parse_number(raw_term)

        elif '/' in raw_term:
            if self.normal_date.match(raw_term):
                self.add_to_dict(raw_term, terms)
            else:
                [self._parse_token_with_number(term, date_buffer, number_buffer, terms) for term in raw_term.split('/')]
        elif '$' in raw_term:
            if re.match("\$\d+b.*|\$\d+\.\d+b.*", raw_term):
                self.add_to_dict((raw_term[raw_term.find("$") + 1:raw_term.find("b")] + " dollar"), terms)
                self.add_to_dict("billion", terms)
            elif re.match("\$\d+m.*|\$\d+\.\d+m.*", raw_term):
                self.add_to_dict((raw_term[raw_term.find("$") + 1:raw_term.find("m")] + " dollar"), terms)
                self.add_to_dict("million", terms)
            else:
                raw_term = raw_term[raw_term.find("$") + 1:]
                self.add_to_dict((self._parse_number(raw_term.replace('$', '')) + " dollar"), terms)
        elif '%' in raw_term:
            self.add_to_dict((self._parse_precentage(raw_term, '%')), terms)
        else:
            self.add_to_dict(raw_term, terms)
        return date_buffer, number_buffer

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

    def add_to_dict(self, term, terms):
        if term in self.stop_words:
            return
        if term not in terms:
            terms[term] = 0
        terms[term] += 1
