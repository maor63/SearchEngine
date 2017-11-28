from datetime import datetime

import nltk.tokenize.simple


class Parser:
    def __init__(self):
        pass

    def parse_token(self, token):
        token = token.replace(',', '')
        if '%' in token:
            return self.parse_precentage(token, '%')
        elif 'percentage' in token:
            return self.parse_precentage(token, 'percentage')
        elif 'percent' in token:
            return self.parse_precentage(token, 'percent')
        return self._parse_number(token)

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
        format = '%{0} %{1} %{2}'
        try:
            return self._parse_day_month_year_date(format, token)
        except ValueError:
            day, month = token.split(' ')
            try:
                return self._parse_day_month_date(day, month, token)
            except ValueError:
                month, year = token.split(' ')
                if len(year) > 2:
                    if len(month) > 3:
                        return self._parse_date_by_format('%B %Y', token, "%m/%Y")
                    else:
                        return self._parse_date_by_format('%b %Y', token, "%m/%Y")
                else:
                    if len(month) > 3:
                        return self._parse_date_by_format('%B %y', token, "%m/%Y")
                    else:
                        return self._parse_date_by_format('%b %y', token, "%m/%Y")


    def _parse_day_month_year_date(self, format, token):
        day, month, year = token.split(' ')
        d = 'd'
        m = 'b'
        if len(year) <= 2:
            y = 'y'
        else:
            y = 'Y'
        if len(day) <= 2:
            if len(month) > 3:
                m = 'B'
            return self._parse_date_by_format(format.format(d, m, y), token)
        else:
            month = day
            if len(month) > 3:
                m = 'B'
            return self._parse_date_by_format(format.format(m, d, y), token)

    def _parse_day_month_date(self, day, month, token):
        if len(day) <= 2:
            if len(month) > 3:
                return self._parse_date_by_format('%d %B', token, "%d/%m")
            else:
                return self._parse_date_by_format('%d %b', token, "%d/%m")
        else:
            if len(day) > 3:
                return self._parse_date_by_format('%B %d', token, "%d/%m")
            else:
                return self._parse_date_by_format('%b %d', token, "%d/%m")
                # return self._parse_date_by_format('%b %d %Y', token)

    def _parse_date_by_format(self, format, token, output_format="%d/%m/%Y"):
        return datetime.strptime(token, format).strftime(output_format)

    def _parse_float(self, f):
        frac_result = str(format(f, ".2f"))
        return frac_result.replace('.00', '')
