def _parse_date2(self, token):
    format = '%{0} %{1}'
    try:
        day, month = token.split(' ')
        d = 'd'
        m = 'b'
        if len(day) <= 2:
            if len(month) > 3:
                m = 'B'
            return self._parse_date_by_format(token, format.format(d, m))
        else:
            month = day
            if len(month) > 3:
                m = 'B'
            return self._parse_date_by_format(token, format.format(m, d))
    except ValueError:
        pass
