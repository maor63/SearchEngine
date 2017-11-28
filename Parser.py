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
            try:
                num, denom = token.split('/')
                frac = float(num) / float(denom)
                return self._parse_float(float(frac))
            except ValueError:
                return self._parse_date(token)

    def _parse_date(self, token):
        token = token.replace('th', '')
        format = '%{0} %{1} %{2}'
        try:
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
        except ValueError:
            pass
            # return self._parse_date_by_format('%b %d %Y', token)

    def _parse_date_by_format(self, format, token):
        return datetime.strptime(token, format).strftime("%d/%m/%Y")

    def _parse_float(self, f):
        frac_result = str(format(f, ".2f"))
        return frac_result.replace('.00', '')
