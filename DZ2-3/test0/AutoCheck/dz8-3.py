from datetime import datetime

date = '2021-05-27 17:08:34.149Z'

def get_str_date(date):
    ls = date.split(' ')
    dt = datetime.strptime(ls[0], '%Y-%m-%d')
    res = dt.strftime('%A %d %B %Y')
    return res

print(get_str_date(date))
