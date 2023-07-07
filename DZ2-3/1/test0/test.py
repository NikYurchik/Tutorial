from random import randrange

class Iterable:
    MAX_VALUE = 10
    def __init__(self):
        self.current_value = 0

    def __next__(self):
        if self.current_value < self.MAX_VALUE:
            self.current_value += 1
            return self.current_value
        raise StopIteration


class CustomIterator:
    def __iter__(self):
        return Iterable()


# c = CustomIterator()
# for i in c:
#     print(i)
#print(randrange(1, 10))
from datetime import datetime
import re
date = '09.08.1958'
#fm = '(\d{4})?(\d{2})?(\d{2})'
def get_date(sdate):
    fmd = ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%d%m%Y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y')
    dt = None
    for fm in fmd:
        try:
            dt = datetime.strptime(sdate, fm)
            break
        except ValueError:
            pass
    if dt == None:
        raise ValueError('The string "{sdate}" is not a date!')
    return dt.date()
print(get_date(date))
